import jmespath

class Config:

    MODE_GET = "get"
    MODE_COMPARE = "compare"

    def __init__(self, config_json):
        self.mode = jmespath.search("mode", config_json) or self.MODE_GET
        self.target_dir = jmespath.search("target_dir", config_json)
        self.compare_dir = jmespath.search("compare_dir", config_json)
        self.explore_name_pairs: list = jmespath.search("explore_name_pairs", config_json) or []
        self.view_name_pairs: list = jmespath.search("view_name_pairs", config_json) or []


    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        mode_list = [
            self.MODE_GET,
            self.MODE_COMPARE
        ]
        if value not in mode_list:
            raise ValueError(f"\"mode\" must be the followings: {', '.join(mode_list)}")
        self.__mode = value


    @property
    def compare_dir(self):
        return self.__compare_dir
    
    @compare_dir.setter
    def compare_dir(self, value):
        if self.mode == self.MODE_COMPARE and value is not None:
            self.__compare_dir = value
        elif self.mode == self.MODE_COMPARE and value is None:
            raise ValueError(f"\"compare_dir\" must be specified when mode is \"{self.MODE_COMPARE}\"")
        elif self.mode != self.MODE_COMPARE and value is not None:
            raise ValueError(f"\"compare_dir\" can be specified only when mode is \"{self.MODE_COMPARE}\"")


    @property
    def explore_name_pairs(self):
        return self.__explore_name_pairs

    @explore_name_pairs.setter
    def explore_name_pairs(self, value):
        if len(value) == 0:
            self.__explore_name_pairs = value
        else:
            if self.mode != 'compare':
                raise ValueError("\"explore_name_pairs\" はmodeが \"compare\" の時のみ指定可能です")
            elif not isinstance(value, list) or not all(isinstance(i, list) for i in value):
                raise ValueError(f"\"explore_name_pairs\" は2重のlist型で指定してください")
            else:
                self.__explore_name_pairs = value


    @property
    def view_name_pairs(self):
        return self.__view_name_pairs

    @view_name_pairs.setter
    def view_name_pairs(self, value):
        if len(value) == 0:
            self.__view_name_pairs = value
        else:
            if self.mode != 'compare':
                raise ValueError("\"view_name_pairs\" はmodeが \"compare\" の時のみ指定可能です")
            elif not isinstance(value, list) or not all(isinstance(i, list) for i in value):
                raise ValueError(f"\"view_name_pairs\" は2重のlist型で指定してください")
            else:
                self.__view_name_pairs = value
