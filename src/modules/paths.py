import sys
from pathlib import Path

class ProjectDirs:
    def __init__(self, prog_name: str):
        if sys.platform == "win32":
            self.config_dir = Path.home() / "AppData" / "Roaming" / prog_name
        elif sys.platform == "linux":
            self.config_dir = Path.home() / ".config" / prog_name
