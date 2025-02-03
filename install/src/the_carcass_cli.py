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
    """
    Exits theSuffocater.

    Returns:
        None: None.
    """

    sys.exit(0)


def the_suffocater_help() -> None:
    """
    Returns theSuffocater commands description and usage.

    Returns:
        None: None
    """

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


def get_markdown(document: str = None) -> None:
    """
    Gets Markdown documents from '/etc/tsf/markdown' and prints them with 'less' command.

    Args:
        document (str): Document specified by user. 'LICENSE.md', 'DOCUMENTATION.md', 'CHANGELOG.md' are available.
        None by default

    Returns:
        None: None.
    """

    try:
        if document is None:
            print(f"{RED}[!] Error: Document not specified.{RESET}")
        else:
            run(["less", f"/etc/tsf/markdown/{document}"], check=True)
    except (FileNotFoundError, CalledProcessError):
        print(f"{RED}[!] Error: '{document}' file not found. Broken installation?{RESET}")


def get_version(component: str = None) -> None:
    """
    Gets version files from '/etc/tsf/versions' (at the top of theCarcass) and prints them.

    Args:
        component (str): theSuffocater component (theCarcass of theSuffocater itself).

    Returns:
        None: None.
    """

    if component is None:
        print(f"{RED}[!] Error: Component not specified.{RESET}")
    
    if component == "theSuffocater":
        print(f"Current theSuffocater version - {the_suffocater_version_string}")

    if component == "theCarcass":
        print(f"Current theCarcass version - {the_carcass_version_string}")


def the_suffocater_neofetch() -> None:
    """
    Prints brief theSuffocater stats.

    Returns:
        None: None.
    """

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


def list_imported_modules(show_docs: bool = False) -> None:
    """
    Lists imported modules and docstrings.

    Args:
        show_docs (bool): If enabled, prints function docstrings too.

    Returns:
        None: None.
    """

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


def import_modules(edit_config: bool = False) -> None:
    """
    Gets path, then imports modules.
    
    Args:
        edit_config (bool): If enabled, enables edit mode.

    Returns:
        None: None.
    """

    directory_path: str = input("[==>] Enter modules directory path (e.g /home/$USER/Desktop/my_python_modules: ")
    if not os.path.isdir(directory_path):
        print(f"{RED}[!] Error: Not a directory.{RESET}")
        return

    import_functions_from_directory(directory_path)


def import_functions_from_directory(directory_path: str) -> None:
    """
    Imports python file functions and docstrings from specified directory
    for further usage in theSuffocater.

    Args:
        directory_path (str): Path to directory with .py files.

    Returns:
        None: None.
    """

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


def import_modules_from_config() -> None:
    """
    Import python modules from config file located in '/etc/tsf/module_configs/import_py.conf'
    using their paths (if exists).
    
    Config file is empty by default.

    Returns:
        None: None.
    """

    config_file_path: str = "/etc/tsf/module_configs/import_py.conf"
    if not os.path.exists(config_file_path):
        print(f"{RED}[!] Error: Configuration file 'import_py.conf' not found!{RESET}")
        return
    
    try:
        with open(config_file_path, "r") as config_file:
            module_paths: list = config_file.readlines()
        
        module_paths: list = [path.strip() for path in module_paths if path.strip() and not path.strip().startswith("#")] 
        if not module_paths:
            print(f"{ORANGE}[!] Error: No module paths found in 'import_py.conf'.{RESET}")
            return

        for directory_path in module_paths:
            if not os.path.isdir(directory_path):
                print(f"{ORANGE}[!] Error: '{directory_path}' is not a valid directory.{RESET}")
                continue
            
            import_functions_from_directory(directory_path)
    except IOError as processing_error:
        print(f"{RED}[!] Error while reading or processing the config file: {processing_error}{RESET}")


def the_carcass(tsf_version_string: str, tc_version_string: str) -> None:
    """
    [*] MAIN FUNCTION [*]
    """

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
            "neofetch": the_suffocater_neofetch,
            "modules -d": lambda: list_imported_modules(show_docs=True),
            "import -e": lambda: import_modules(edit_config=True)
            "license": lambda: get_markdown(document="LICENSE-GPL.md"),
            "changelog": lambda: get_markdown(document="CHANGELOG.md"),
            "documentation": lambda: get_markdown(document="README.md"),
            "tsf_version": lambda: get_version(component="theSuffocater"),
            "tc_version": lambda: get_version(component="theCarcass")
    }
    
    tum.clear_screen()
    import_modules_from_config()
    the_carcass(tsf_version_string=the_suffocater_version_string, tc_version_string=the_carcass_version_string)
