import regex

from classes.field import Field
from classes.lookml_common import (
    get_params_with_parentheses,
    get_relative_path
)
from classes.util import *

class View:

    def __init__(self, name: str, content: str, filepath: str, base_dir: str):
        self.name: str = name
        self.content: str = content
        self.filepath: str = get_relative_path(filepath, base_dir)
        self.dimensions: list[Field] = self.get_fields(param="dimension")
        self.measures: list[Field] = self.get_fields(param="measure")
        self.filters: list[Field] = self.get_fields(param="filter")
        self.parameter: list[Field] = self.get_fields(param="parameter")
        self.dimension_group: list[Field] = self.get_fields(param="dimension_group")
        self.content_without_fields: str = self.get_content_without_fields()
        self.label: str = self.get_label()
        self.view_label: str = self.get_view_label()
        self.sql_table_name: str = self.get_sql_table_name()
        self.derived_table: str = self.get_derived_table()
        self.derived_table_sql: str = self.get_derived_table_sql()
    

    def get_fields(self, param) -> list[Field]: # type: ignore
        fields: list[Field] = []
        for matches in get_params_with_parentheses(self.content, param):
            fields.append(Field(param, matches[0], matches[1]))
        return fields
    

    def get_content_without_fields(self) -> str:
        content = self.content
        for field in self.dimensions + self.measures + self.filters + self.parameter + self.dimension_group:
            content = content.replace(field.content, "")
        return content
    

    def get_label(self):
        result: re.Match = re.search(r"\s+label\s*:\s*[\'\"](.+)[\'\"]", self.content_without_fields)
        return result.group(1) if result else None
    

    def get_view_label(self) -> str:
        result: re.Match = re.search(r"\s+view_label\s*:\s*[\'\"](.+)[\'\"]", self.content_without_fields)
        return result.group(1) if result else None
    

    def get_sql_table_name(self) -> str:
        result: re.Match = re.search(r"\s+sql_table_name\s*:([\s\S]+);;", self.content_without_fields)
        return result.group(1).strip() if result else None
    

    def get_derived_table(self) -> str:
        matches_list = regex.findall(r"derived_table\s*:\s*(?<rec>\{(?:[^\{\}]+|(?&rec))*\})", self.content_without_fields)
        return matches_list[0] if len(matches_list) > 0 else None
    

    def get_derived_table_sql(self) -> str:
        if self.derived_table is None:
            return None
        else:
            result: re.Match = re.search(r"\s+sql\s*:([\s\S]+);;", self.derived_table)
            return result.group(1).strip() if result else None
