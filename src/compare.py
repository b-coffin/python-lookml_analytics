import os

from classes.sqlite3 import SQLite3


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
