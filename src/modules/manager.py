import os
import sys
import json

from glob import glob
from subprocess import Popen
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
        self.dir_name = os.path.split(path)[1]
        self.description = self.__config["description"]

class Fnf:
    def __init__(self, path: str):
        if os.path.exists(path) is True\
        and os.path.isdir(path) is True:
            self.path = path
        else:
            raise FileNotFoundError()

        self.mod_dir = os.path.join(self.path, "mods")

    def get_active_mod(self) -> Mod:
        return Mod(self.mod_dir)

    def set_active_mod(self, mod: str | Mod):
        """
        Parameters:
            name (str): The folder name of the mod, the mod should be in the root directory
        """
        mod_dir = mod.dir_name if isinstance(mod, Mod) else mod

        if os.path.exists(self.mod_dir):
            _mod = self.get_active_mod()
            os.rename(self.mod_dir, os.path.join(self.path, _mod.name.replace(" ", "_")))

        os.rename(os.path.join(self.path, mod_dir), os.path.join(self.path, "mods"))

    def get_mods(self) -> list[Mod]:
        packs_json = glob(os.path.join(self.path, "**", "pack.json"))
        if len(packs_json) == 0:
            return []

        return [Mod(os.path.split(pack)[0]) for pack in packs_json]

    def run(self):
        runner = CONFIG.get_runner()
        if runner == "native":
            e = listExecutables(self.path)
            if len(e) > 1:
                print("There is more than one executable file in the psychEngine folder")
                return
            os.system(e[0])

        elif runner == "bottles":
            e = listExecutables(self.path, platform="win32")

            bottle = []
            if CONFIG._config["runnerConfig"]["bottle"] != "":
                bottle = ["-b",CONFIG._config["runnerConfig"]["bottle"]]

            Popen(args=["flatpak", "run", "com.usebottles.bottles", *bottle, e[0]],
                cwd=self.path,
                stdout=sys.stdout,
                stderr=sys.stderr
            ).communicate()

        elif runner == "wine":
            e = listExecutables(self.path, platform="win32")

            prefix = CONFIG._config['runnerConfig']['winePrefix'].replace("~", os.environ['HOME'])
            _env = {"WINEPREFIX": prefix}
            _env.update(os.environ)

            Popen(args=["wine", e[0]],
                # env=_env,
                cwd=self.path,
                stdout=sys.stdout,
                stderr=sys.stderr
            ).communicate()
        else:
            print("Invalid runner")
