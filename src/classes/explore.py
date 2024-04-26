import glob
import re

from classes.lookml_common import (
    get_params_with_parentheses,
    get_relative_path
)
from classes.util import *
from classes.view import View

class Explore:

    def __init__(self, name: str, content: str, filepath: str, base_dir: str, includes: list[str]): # type: ignore
        self.name: str = name
        self.content: str = content
        self.filepath: str = get_relative_path(filepath, base_dir)
        self.includes: list[str] = includes
        self.label: str = self.get_label()
        self.view_name: str = self.get_view_name()
        self.joins: list[str] = self.get_joins()
        self.views: list[View] = self.get_views(base_dir)
    

    def get_label(self) -> str|None:
        result: re.Match = re.search(r"\s+label\s*:\s*[\'\"](.+)[\'\"]", self.content)
        return result.group(1) if result else None
    

    def get_view_name(self) -> str|None:
        result: re.Match = re.search(r"\s+view_name\s*:\s*(.+)", self.content)
        return result.group(1) if result else None
    

    def get_joins(self) -> list[str]: # type: ignore
        joins: list[str] = []
        for matches in get_params_with_parentheses(self.content, "join"):
            joins.append(matches[0])
        return joins
        

    def get_views(self, base_dir: str) -> list[View]: # type: ignore
        views: list[View] = []
        for include in self.includes:
                for path in glob.glob(include, recursive=True):
                    with open(path, "r") as f:
                        content = f.read()
                        for matches in get_params_with_parentheses(content, "view"):
                            if matches[0] in self.joins + [self.view_name]:
                                views.append(View(matches[0], matches[1], path, base_dir))
        return views
