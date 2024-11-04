import json
import os

CONFIG_PATH = os.path.join(os.environ['HOME'], ".config", "fmm", "fmm.json")
CONFIG = {
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

    with open(CONFIG_PATH, "w") as _c:
        json.dump(CONFIG, _c, indent=4)
else:
    with open(CONFIG_PATH, "r") as _c:
        CONFIG = json.load(_c)
