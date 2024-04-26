import os
import sqlite3

from typing import Tuple

from classes.util import *

class SQLite3:

    def __init__(self, dbname):
        os.makedirs(os.path.dirname(dbname), exist_ok=True)
        self.connect: sqlite3.Connection = sqlite3.connect(dbname)
        self.cursor: sqlite3.Cursor = self.connect.cursor()


    def close(self):
        self.cursor.close()
        self.connect.close()


    def commit(self):
        self.connect.commit()


    def create_temp_table(self, table_name: str, columns: list[str]) -> None: # type: ignore
        sql = f"CREATE TEMPORARY TABLE {table_name} ({", ".join(columns)})"
        self.cursor.execute(sql)


    def insert_allcolumns(self, table_name: str, columns: list[str], values: list[Tuple]) -> None: # type: ignore
        self.cursor.executemany(f"INSERT INTO {table_name} VALUES({', '.join(['?'] * len(columns))})", values)


    def clease_selectresult_to_list(self, columns: list[str]) -> list[Tuple]: # type: ignore
        result = self.cursor.fetchall()
        result.insert(0, tuple(columns))
        return result


    def select_all(self, table_name: str, columns: list[str]) -> list[dict]: # type: ignore
        sql = f"SELECT * FROM {table_name}"
        self.cursor.execute(sql)
        return self.clease_selectresult_to_list(columns)


    def select_for_compare(self, left_tbl_name: str, right_tbl_name: str, columns: list[str], keys_list: list[list]) -> list[dict]: # type: ignore

        # join句を作成
        if len(keys_list) == 0:
            join_condition: str = "ON TRUE"
        else:
            joins: list[str] = []
            for keys in keys_list:
                joins.append(" OR ".join([f"{left_tbl_name}.{key} = {right_tbl_name}.{key}" for key in keys]))
            join_condition: str = "ON (" + ")\n\tAND (".join(joins) + ")"

        sql = get_text_used_jinja2template(
            os.path.join("templates", "sql", "compare", "select.sql"),
            {
                "left_tbl_name": left_tbl_name,
                "right_tbl_name": right_tbl_name,
                "join_condition": join_condition
            }
        )
        self.cursor.execute(sql)

        return self.clease_selectresult_to_list([f"{col}_{left_tbl_name}" for col in columns] + [f"{col}_{right_tbl_name}" for col in columns])
