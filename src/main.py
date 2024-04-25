import os
import traceback

from classes.config import Config
from classes.util import *
from compare import get_merged_result
from get import get_result_for_csv


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
