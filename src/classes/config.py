import jmespath

class Config:

    MODE_GET = "get"
    MODE_COMPARE = "compare"

    def __init__(self, config_json):
        self.mode = jmespath.search("mode", config_json) or self.MODE_GET
        self.target_dir = jmespath.search("target_dir", config_json)
        self.compare_dir = jmespath.search("compare_dir", config_json)
        self.bq_project = jmespath.search("bq.project", config_json)
        self.bq_dataset = jmespath.search("bq.dataset", config_json)


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
