import jmespath

class Config:

    MODE_GET = "get"
    MODE_COMPARE = "compare"

    def __init__(self, config_json):
        self.mode = jmespath.search("mode", config_json) or self.MODE_GET
        self.target_dir = jmespath.search("target_dir", config_json)
        self.compare_dir = jmespath.search("compare_dir", config_json)
        self.target_explore = jmespath.search("target_explore", config_json)
        self.compare_explore = jmespath.search("compare_explore", config_json)

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
    def compare_explore(self):
        return self._compare_explore
    
    @compare_explore.setter
    def compare_explore(self, value):
        if self.mode == self.MODE_COMPARE and self.target_explore is not None and value is None:
            raise ValueError(f"\"compare_explore\" は、mode が \"{self.MODE_COMPARE}\" で compare_dir が指定されている場合は必須です: ")
        elif self.mode != self.MODE_COMPARE and value is not None:
            raise ValueError(f"\"compare_explore\" は、右記modeの時のみ指定することができます: \"{self.MODE_COMPARE}\"")
        else:
            self._compare_explore = value
