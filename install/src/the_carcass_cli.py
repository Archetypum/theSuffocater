#!/usr/bin/python3  
#
# This thing is called "theCarcass" - heart of theSuffocater.
# theCarcass destiny is to load modules and scripts from directories provided by the user.
# for further using.
#
# Usually theCarcass don't receive many updates because it's already serving
# its functionality very good, but not in current release! Say hello to new theCarcass-2.0!
#
# Graphical frontend - the_carcass_gui.py
# Bash version - the_carcass_cli.sh

try:
    print(f"[==>] Importing python modules...")
    import os
    import sys
    import inspect
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


def final_exit() -> None:
    sys.exit(0)


def the_suffocater_help() -> None:
    print("\nCommands:")
    print(" exit - exit theSuffocater.")
    print(" clear - clear the screen.")
    print(" help - display this message.")
    print(" neofetch - brief theSuffocater statistics.")
    print(" import - for importing modules from directories.")
    print(" modules [-d] - list imported modules. '-d' argument for documentation.")
    print(" tsf_version - get current version of theSuffocater.")
    print(" tc_version - get current version of theCarcass.")
    print(" license - check license.")
    print(" documentation - check readme")
    print(" changelog - check whats new in your current version")
    print("\nFor more info, check 'documentation'.")


def the_suffocater_version() -> None:
    print(f"Current theSuffocater version - {the_suffocater_version_string}")


def the_suffocater_license() -> None:
    try:
        run(["less", "LICENSE-GPL.md"], check=True)
    except (FileNotFoundError, CalledProcessError):
        print(f"{RED}[!] Error: 'LICENSE.md' file not found. Broken installation?")


def the_suffocater_changelog() -> None:
    try:
        run(["less", "CHANGELOG.md"], check=True)
    except (FileNotFoundError, CalledProcessError):
        print(f"{RED}[!] Error: 'CHANGELOG.md' file not found. Broken installation?")


def the_suffocater_documentation() -> None:
    try:
        run(["less", "README.md"], check=True)
    except (FileNotFoundError, CalledProcessError):
        print(f"{RED}[!] Error: 'README.md' file not found. Broken installation?")


def the_suffocater_neofetch() -> None:
    print(f"""
{BLUE}
                 __________           {RESET}theSuffocater version - {GREEN}{the_suffocater_version_string}{BLUE}
                [0000000000]          {RESET}Loaded modules - ...{BLUE}
            [0000000000000000.
          [000000]         .  .       {RESET}Adapted distributions count - {GREEN}{distros_count}{BLUE}
         [00000]           [000]      {RESET}Current contributors - {GREEN}{the_suffocater_contributors}{BLUE}
       [00000]             [000]      {BLACK}███{WHITE}███{YELLOW}███{ORANGE}███{BLUE}
       [00000]          [0000000000]  {GREEN}███{RED}███{BLUE}███{PURPLE}███{BLUE}
       [0000]            ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺
        [00000.   ____
         [0000.  .0000]
            [0.  .000000.   __
             ⎺   .000000.  .00]
                     [00.  .0000]
      __________      ⎺⎺   [00000]
     [0000000000]          [00000]
        [000]              [00000]
        [000]             [00000]
         .  .           [000000]
          .0000000000000000]
              [0000000]
               ⎺⎺⎺⎺⎺⎺⎺ {RESET}
""")


def the_carcass_version() -> None:
    print(f"Current theCarcass version - {the_carcass_version_string}")


def list_imported_modules(show_docs: bool = False) -> None:
    print(f"+{'-' * 15} Imported modules {'-' * 15}+")
    for module_path, module_info in loaded_modules.items():
        print(f"\n  -> Path: {module_path}")
        if show_docs:
            print(f"  -> Docstring: {module_info['docstring'] or 'None'}")
        print("  --> Functions:")
        for func_name, func_docstring in module_info["functions"].items():
            if show_docs:
                print(f"    - {func_name}: {func_docstring or 'None'}")
            else:
                print(f"    - {func_name}")


def import_modules() -> None:
    directory_path: str = input("[==>] Enter modules directory path (e.g /home/$USER/Desktop/my_python_modules: ")
    if not os.path.isdir(directory_path):
        print(f"{RED}[!] Error: Not a directory.{RESET}")
        return

    import_functions_from_directory(directory_path)


def import_functions_from_directory(directory_path: str) -> None:
    for filename in os.listdir(directory_path):
        if filename.endswith(".py"):
            file_path: str = os.path.join(directory_path, filename)
            try:
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if file_path in loaded_modules:
                    del loaded_modules[file_path]
                    
                loaded_modules[file_path] = {
                    "docstring": module.__doc__,
                    "functions": {}
                }
                
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj):
                       loaded_modules[file_path]["functions"][name] = obj.__doc__
                       default_modules[name] = obj

                print(f"{BLUE}[<==] Imported module from: {file_path}{RESET}") 
            except FileNotFoundError as module_import_error:
                print(f"{RED}[!] Error: Can't import module from {file_path}:\n{module_import_error}")


def the_carcass(tsf_version_string: str, tc_version_string: str) -> None:
    print(f"+{'-' * 16} Welcome to theSuffocater {'-' * 16}+\n")
    print(f" Current tSF version - {tsf_version_string}")
    print(f" Current tC version - {tc_version_string}\n")
    print(f"+{'-' * 58}+")

    while True:
        try:
            command: str = input(f"{PURPLE}\n(root){RESET} -> # ").lower().strip()
            if not command:
                continue
        
            if command in default_modules:
                default_modules[command]()
        
            else:
                print(f"{RED}[!] Error: Module not found.")
                print(f"Please check the name or ensure it is imported and try 'help'.{RESET}")
        except KeyboardInterrupt:
            print("\n")
            final_exit()


if __name__ == "__main__":
    default_modules: dict = {
            "exit": final_exit,
            "clear": tum.clear_screen,
            "help": the_suffocater_help,
            "import": import_modules,
            "modules": list_imported_modules,
            "modules -d": lambda: list_imported_modules(show_docs=True),
            "neofetch": the_suffocater_neofetch,
            "license": the_suffocater_license,
            "changelog": the_suffocater_changelog,
            "documentation": the_suffocater_documentation,
            "tsf_version": the_suffocater_version,
            "tc_version": the_carcass_version
    }
    tum.clear_screen()
    the_carcass(tsf_version_string=the_suffocater_version_string, tc_version_string=the_carcass_version_string)
