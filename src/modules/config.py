import json
import os
from typing import Literal
from .paths import ProjectDirs

dirs = ProjectDirs("fmm")
CONFIG_PATH = str(dirs.config_dir / "fmm.json")

class Config:
    def __init__(self):
        self._config = {
            "executableInstalledMods": [],
            "psychEnginePath": "",
            "runner": "native",

            "runnerConfig": {
                "bottle": "",
                "winePrefix": "~/.wine"
            },

            "aliases": {}
        }
        if os.path.exists(CONFIG_PATH) is False:
            os.makedirs(os.path.split(CONFIG_PATH)[0], exist_ok=True)
            self.save()
        else:
            with open(CONFIG_PATH, "r") as _c:
                self._config = json.load(_c)

    def set_psych_engine_path(self, path: str):
        if os.path.exists(path):
            self._config["psychEnginePath"] = path
        else:
            raise FileNotFoundError(path, "doesn't exists")

    def get_psych_engine_path(self):
        return self._config["psychEnginePath"]

    def new_alias(self, name, mod_path):
        if os.path.exists(mod_path):
            self._config["aliases"][name] = mod_path
        else:
            raise FileNotFoundError(mod_path, "doesn't exists")

    def get_aliases(self) -> dict:
        return self._config["aliases"]

    def get_alias(self, alias: str):
        return self._config["aliases"][alias]

    def get_installed_mods(self):
        return self._config["executableInstalledMods"]

    def get_runner(self):
        return self._config["runner"]

    def set_runner(self, runner: Literal["native", "wine", "bottles"]):
        if runner not in ["native", "wine", "bottles"]:
            raise ValueError("Invalid runner")

    def save(self):
        with open(CONFIG_PATH, "w") as _c:
            json.dump(self._config, _c, indent=4)

CONFIG = Config()
