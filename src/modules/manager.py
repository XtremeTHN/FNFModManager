import os
import sys
import json

from glob import glob
from typing import TypedDict
from .config import CONFIG, CONFIG_PATH

def listExecutables(path: str, platform=sys.platform):
    def checkIfExec(file):
        if platform == "linux":
            if os.path.isfile(file) and os.access(file, os.X_OK):
                return True
        elif platform == "win32":
            if os.path.splitext(file)[1] == ".exe":
                return True
        return False

    f = []
    for filename in os.listdir(path):
        executable = checkIfExec(filename)
        if executable is True:
            f.append(os.path.join(path, filename))

    return f

def add_alias(name: str, path: str):
    CONFIG["aliases"][name] = path
    with open(CONFIG_PATH, "w") as f:
        json.dump(CONFIG, f)

def get_alias(name: str) -> str:
    return CONFIG["aliases"][name]

class ModInfo(TypedDict):
    name: str
    description: str
    restart: bool
    color: list[int]

class Mod:
    def __init__(self, path: str):
        if os.path.exists(path) is True:
            self.path = path
        else:
            raise FileNotFoundError("The mod path doesn't exists")

        with open(os.path.join(path, "pack.json"), "r") as f:
            self.__config: ModInfo = json.load(f)

        self.name = self.__config["name"]
        self.description = self.__config["description"]

class Fnf:
    def __init__(self, path: str):
        if os.path.exists(path) is True\
        and os.path.isdir(path) is True:
            self.path = path
        else:
            raise FileNotFoundError()

        self.mods_dir = os.path.join(self.path, "mods")

    def get_active_mod(self) -> Mod:
        return Mod(self.mods_dir)

    def set_active_mod(self, mod: str | Mod):
        """
        Parameters:
            name (str): The folder name of the mod, the mod should be in the root directory
        """
        name = mod.name if isinstance(mod, Mod) else mod

        if os.path.exists(self.mods_dir):
            _mod = self.get_active_mod()
            os.rename(self.mods_dir, _mod.name.replace(" ", "_"))

        os.rename(os.path.join(self.path, name), "mods")

    def get_mods(self) -> list[Mod]:
        packs_json = glob(os.path.join(self.path, "**", "pack.json"))
        if len(packs_json) == 0:
            return []

        return [Mod(os.path.split(pack)[0]) for pack in packs_json]

    def run(self):
        if CONFIG["runner"] == "native":
            e = listExecutables(self.path)
            if len(e) > 1:
                print("There is more than one executable file in the psychEngine folder")
                return
            os.system(e[0])

        elif CONFIG["runner"] == "bottles":
            e = listExecutables(self.path, platform="win32")

            bottle = ""
            if CONFIG["runnerConfig"]["bottle"] != "":
                bottle = " -b " + CONFIG["runnerConfig"]["bottle"]
            os.system(f"flatpak run com.usebottles.bottles" + bottle + f" {e[0]}")

        elif CONFIG["runner"] == "wine":
            e = listExecutables(self.path, platform="win32")

            os.system(f"WINEPREFIX={CONFIG['runnerConfig']['winePrefix']} wine {e[0]}")
        else:
            print("Invalid runner")
