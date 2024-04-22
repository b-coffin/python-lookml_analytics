import re

class Field:

    def __init__(self, param, name, content):
        self.param = param
        self.name = name
        self.content = content
        self.label = self.get_label()
        self.hidden = self.get_hidden()


    def get_label(self):
        result: re.Match = re.search(r"\s+label\s*:\s*[\'\"](.+)[\'\"]", self.content)
        return result.group(1) if result else None
    

    def get_hidden(self) -> str:
        result: re.Match = re.search(r"\s+hidden\s*:\s*(yes|no)", self.content)
        return result.group(1) if result else "no"
