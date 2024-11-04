import os
import sys

from modules.config import CONFIG
from modules.manager import Fnf, add_alias, get_alias

match sys.argv[1]:
    case "psych":
        if os.path.exists(CONFIG["psychEnginePath"]) is False:
            print(f'Error: "{CONFIG["psychEnginePath"]}" does not exists')
            print("Set the psychEnginePath correctly")
            sys.exit(1)
        path = CONFIG["psychEnginePath"]
        fnf = Fnf(path)

        match sys.argv[2]:
            case "list":
                print("Installed mods in psychEngine:")
                print("\n".join([m.name for m in fnf.get_mods()]))

            case "active-mod":
                print("Current mod:", fnf.get_active_mod().name)

            case "run":
                if len(sys.argv) > 3:
                    mods = fnf.get_mods()
                    mod_names = [m.name for m in mods]
                    try:
                        mod_pos = mod_names.index(sys.argv[3])
                    except ValueError:
                        print(f'"{sys.argv[3]}"', "is not installed")
                        sys.exit(1)

                    fnf.set_active_mod(mods[mod_pos])

                fnf.run()

    case "add-alias":
        if os.path.exists(sys.argv[3]) is False:
            print("Mod doesn't exist")
            sys.exit(1)

        add_alias(sys.argv[2], sys.argv[3])

    case "start":
        fnf = Fnf(get_alias(sys.argv[2]))
        fnf.run()
