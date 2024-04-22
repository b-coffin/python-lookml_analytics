import os
import traceback

from typing import Tuple

from classes.config import Config
from classes.explore import Explore
from classes.lookml_common import get_includes, get_params_with_parentheses
from classes.sqlite3 import SQLite3
from classes.util import *


def get_explores(path: str, base_dir: str) -> list[Explore]: # type: ignore
    explores: list[Explore] = []
    with open(path, "r") as f:
        content = f.read()
        for matches in get_params_with_parentheses(content, "explore"):
            explores.append(Explore(matches[0], matches[1], path, base_dir, get_includes(content)))
    return explores


def get_result_for_csv(base_dir: str, input_filenames: list[str]) -> Tuple[list[dict], list[dict], list[dict]]: # type: ignore
    explores: list[dict] = []
    views: list[dict] = []
    fields: list[dict] = []

    for file in input_filenames:
        print_with_color(f"\n### {file}", COLOR_BLUE)

        exps = get_explores(file, base_dir)
        
        for exp in exps:
            explores.append({
                "name": exp.name,
                "label": exp.label,
                "filepath": exp.filepath
            })
            for view in exp.views:
                views.append({
                    "explore_name": exp.name,
                    "explore_label": exp.label,
                    "view_name": view.name,
                    "view_label": view.label or view.view_label or view.name,
                    "sql_table_name": view.sql_table_name,
                    "derived_table_sql": view.derived_table_sql,
                    "view_filepath": view.filepath
                })
                for field in view.dimensions + view.measures + view.filters:
                    fields.append({
                        "explore_name": exp.name,
                        "explore_label": exp.label,
                        "view_name": view.name,
                        "view_label": view.label or view.view_label or view.name,
                        "field_name": field.name,
                        "field_label": field.label or field.name,
                        "hidden": field.hidden
                    })

        print_with_color("...Done", COLOR_GREEN)

    return explores, views, fields


def get_merged_result(left: list[dict], right: list[dict], keys_list: list[list]) -> list[dict]: # type: ignore
    sqlite3 = SQLite3(os.path.join("db", "dummy.db"))

    columns: list[str] = list(left[0].keys())

    left_tbl_name: str = "left"
    sqlite3.create_temp_table(left_tbl_name, columns)
    sqlite3.insert_allcolumns(left_tbl_name, columns, [tuple(row.values()) for row in left])
    sqlite3.commit()

    right_tbl_name: str = "right"
    sqlite3.create_temp_table(right_tbl_name, columns)
    sqlite3.insert_allcolumns(right_tbl_name, columns, [tuple(row.values()) for row in right])
    sqlite3.commit()

    result = sqlite3.select_for_compare(
        left_tbl_name=left_tbl_name,
        right_tbl_name=right_tbl_name,
        columns=columns,
        keys_list=keys_list
    )

    sqlite3.close()
    return result


def main():

    default_config_file: str = "sample_get.json"
    config_filepath: str = os.path.join(os.path.dirname(__file__), "config", input(f"Input config file name (default: {default_config_file}) : ") or default_config_file)
    config_json: dict = read_jsonfile(config_filepath)

    # configのバリデーションチェック
    try:
        config: Config = Config(config_json)
    except Exception:
        print(f"Stacktrace: {traceback.format_exc()}")

    # inputフォルダ配下で、指定したフォルダ配下のファイルをすべて精査
    input_dir: str = os.path.join(os.path.dirname(__file__), "input", config.target_dir)
    input_filenames: list[str] = get_filenames(input_dir, extensions=["lkml", "txt"], words=[])

    explores, views, fields = get_result_for_csv(input_dir, input_filenames)

    result_dir = os.path.join(os.path.dirname(__file__), "result", f"{get_nowdatetime()}_{config.mode}")

    if config.mode == Config.MODE_GET:
        write_dicts_to_csv(os.path.join(result_dir, "explores.csv"), explores)
        write_dicts_to_csv(os.path.join(result_dir, "views.csv"), views)
        write_dicts_to_csv(os.path.join(result_dir, "fields.csv"), fields)

    if config.mode == Config.MODE_COMPARE:
        print_with_color("\n### compare\n", COLOR_BLUE)

        compare_dir: str = os.path.join(os.path.dirname(__file__), "input", config.compare_dir)
        compare_filenames: list[str] = get_filenames(compare_dir, extensions=["lkml", "txt"], words=[])

        compare_explores, compare_views, compare_fields = get_result_for_csv(compare_dir, compare_filenames)

        write_csv(os.path.join(result_dir, "explores.csv"), get_merged_result(
            left=explores,
            right=compare_explores,
            keys_list=[["label", "name"]]
        ))

        write_csv(os.path.join(result_dir, "views.csv"), get_merged_result(
            left=views,
            right=compare_views,
            keys_list=[["explore_name", "explore_label"], ["view_name", "view_label"]]
        ))

        write_csv(os.path.join(result_dir, "fields.csv"), get_merged_result(
            left=fields,
            right=compare_fields,
            keys_list=[["explore_name", "explore_label"], ["field_name", "field_label"]]
        ))


# メイン
if __name__ == "__main__":
    main()
