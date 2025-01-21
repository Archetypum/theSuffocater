#!/usr/bin/python3
#
# This thing is called "theCarcass" - heart of theSuffocater.
# theCarcass destiny is to load modules and scripts from directories provided by the user.
# for further using.
#
# Usually theCarcass don't receive many updates because it's already serving
# its functionality very good, but not in current release! Say hello to new theCarcass-2.0!
#
# CLI version - the_carcass_gui.py

try:
    print(f"[==>] Importing python modules...")
    import os
    import sys
    import inspect
    import tkinter as tk
    import importlib.util
    import the_unix_manager as tum
    from subprocess import run, CalledProcessError
    from the_unix_manager import GREEN, RED, PURPLE, BLACK, WHITE, YELLOW, ORANGE, BLUE, RESET
except ModuleNotFoundError as import_error:
    print(f"[!] Error: Modules not found. Broken installation?\n\n{import_error}")
    sys.exit(1)
finally:
    print(f"{GREEN}[*] Python modules are successfully imported. Loading theSuffocater global variables...{RESET}")

try:
    distros_count: int = 52
    the_suffocater_contributors: float = 3.5
    current_directory: str = os.path.dirname(__file__)
    loaded_modules: dict = {}
    with open("/etc/tsf/versions/tsf_version.txt", "r") as tsf_version_file:
        the_suffocater_version_string: str = tsf_version_file.read().strip()
    with open("/etc/tsf/versions/tc_version.txt", "r") as tc_version_file:
        the_carcass_version_string: str = tc_version_file.read().strip()
except FileNotFoundError as variable_error:
    print(f"{RED}[!] Error: Failed to create global variables:\n\n{variable_error}{RESET}")
    sys.exit(1)
finally:
    print(f"{GREEN}[*] Variables are successfully initialized. Loading main function...{RESET}")
