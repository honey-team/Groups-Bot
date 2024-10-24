import json
from typing import Any

PATH_TO_CONFIG_FILE = "data/config.json"

class __Config(dict):
    def __init__(self):
        super().__init__()
        self.__cache__ = {}
        self.update_cache()
    
    def update_cache(self):
        with open(PATH_TO_CONFIG_FILE, "rb") as cf:
            self.__cache__ = json.load(cf)
    
    def __getitem__(self, key: str) -> (Any | None):
        if isinstance(key, str):
            return self.__cache__[key]
        else:
            raise TypeError()
        
Config = __Config()

__all__ = (
    "Config",
    "PATH_TO_CONFIG_FILE"
)
