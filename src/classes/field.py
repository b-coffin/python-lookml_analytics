import re

class Field:

    def __init__(self, param, name, content):
        self.param = param
        self.name = name
        self.content = content
        self.label: str|None = self.get_label()
        self.group_label: str|None = self.get_group_label()
        self.hidden: str = self.get_hidden()
        self.type: str|None = self.get_type()
        self.sql: str|None = self.get_sql()


    def get_label(self) -> str|None:
        result: re.Match = re.search(r"\s+label\s*:\s*[\'\"](.+)[\'\"]", self.content)
        return result.group(1) if result else None
    

    def get_group_label(self) -> str|None:
        result: re.Match = re.search(r"\s+group_label\s*:\s*[\'\"](.+)[\'\"]", self.content)
        return result.group(1) if result else None
    

    def get_hidden(self) -> str:
        result: re.Match = re.search(r"\s+hidden\s*:\s*(yes|no)", self.content)
        return result.group(1) if result else "no"


    def get_type(self) -> str|None:
        result: re.Match = re.search(r"\s+type\s*:\s*(\S+)", self.content)
        return result.group(1) if result else None


    def get_sql(self) -> str|None:
        result: re.Match = re.search(r"sql\s*:\s*([\s\S]+?);;", self.content)
        return result.group(1).strip() if result else None
