#!/usr/bin/env python3
import os
import sys

from modules.config import CONFIG
from modules.style import bold, underlined, error, info
from modules.manager import Fnf

def print_usage():
    print("usage: fmm [OPERATION] [-h]")

def print_help():
    print_usage()
    print("\nFriday Night Funkin' mod manager")
    print(bold(underlined("Operations:")))
    print("\tpsych: Psych engine related commands")
    print("\talias: Alias related commands")
    print("\tstart: Executes a mod with the alias")

def print_help_psych():
    print_usage()
    print("\nFriday Night Funkin' mod manager")
    print(bold(underlined("Operations:")))
    print("\tlist: List installed mods in the psych engine folder")
    print("\tactive-mod: Print the active psych engine mod")
    print("\trun [MOD_FOLDER_NAME]: Runs the psych engine with the specified mod")

def print_help_alias():
    print_usage()
    print("\nFriday Night Funkin' mod manager")
    print(bold(underlined("Operations:")))
    print("\tnew: Creates a new alias, requires the name of the alias and the mod path")
    print("\tremove: Removes an alias")
    print("\tlist: List the available aliases")

if len(sys.argv) < 2:
    print_help()
    sys.exit(0)

match sys.argv[1]:
    case "help" | "-h" | "--help":
        print_help()

    case "psych":
        path = CONFIG.get_psych_engine_path()

        if os.path.exists(path) is False:
            error(f'"{path}" does not exists')

        fnf = Fnf(path)
        if len(sys.argv) < 3:
            error("Expected command")

        match sys.argv[2]:
            case "help" | "-h" | "--help":
                print_help_psych()
            case "list":
                print(bold(underlined("Installed mods in psychEngine:")))
                print("\n".join([m.name for m in fnf.get_mods()]))

            case "set-psych-path":
                if len(sys.argv) < 3:
                    error("Expected psych path")

                CONFIG.set_psych_engine_path(sys.argv[2])
            case "active-mod":
                print(bold("Current mod:"), fnf.get_active_mod().name)

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

    case "alias":
        if len(sys.argv) < 3:
            error("Expected command.")

        match sys.argv[2]:
            case "new":
                if len(sys.argv) < 4:
                    error("Expected alias name and mod path")
                if len(sys.argv) < 5:
                    error("Expected mod path")

                if os.path.exists(sys.argv[4]) is False:
                    print("Mod doesn't exist")
                    sys.exit(1)

                print(sys.argv)
                CONFIG.new_alias(sys.argv[3], sys.argv[4])

            case "list":
                info("List of existing aliases:")
                for alias_name in CONFIG.get_aliases():
                    print("\t" + alias_name, "->", CONFIG.get_aliases()[alias_name])
                sys.exit(0)

    case "start":
        fnf = Fnf(CONFIG.get_alias(sys.argv[2]))
        fnf.run()

    case _:
        print("usage: fmm [OPERATION]")
