from typing import Tuple

from classes.explore import Explore
from classes.lookml_common import (
    get_params_with_parentheses,
    get_includes
)
from classes.util import (
    COLOR_BLUE,
    COLOR_GREEN,
    print_with_color
)

def get_explores(path: str, base_dir: str, target_explore: str|None) -> list[Explore]: # type: ignore
    explores: list[Explore] = []
    with open(path, "r") as f:
        content = f.read()
        for matches in get_params_with_parentheses(content, "explore"):
            explore_name = matches[0]
            if target_explore is None or target_explore == explore_name:
                explores.append(Explore(matches[0], matches[1], path, base_dir, get_includes(content, base_dir)))
    return explores


def get_result_for_csv(base_dir: str, input_filenames: list[str], target_explore: str|None) -> Tuple[list[dict], list[dict], list[dict]]: # type: ignore
    explores: list[dict] = []
    views: list[dict] = []
    fields: list[dict] = []

    for file in input_filenames:
        print_with_color(f"\n### {file}", COLOR_BLUE)

        exps = get_explores(file, base_dir, target_explore)
        
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
                        "group_label": field.group_label,
                        "field_name": field.name,
                        "field_label": field.label or field.name,
                        "hidden": field.hidden
                    })

        print_with_color("...Done", COLOR_GREEN)

    return explores, views, fields
