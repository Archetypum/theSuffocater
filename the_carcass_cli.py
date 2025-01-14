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


def final_exit() -> None:
    sys.exit(0)


def the_suffocater_help() -> None:
    print("\nCommands:")
    print(" exit - exit theSuffocater.")
    print(" clear - clear the screen.")
    print(" help - display this message.")
    print(" neofetch - brief theSuffocater statistics.")
    print(" modules [-d] - list imported modules (use -d to include documentation).")
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
        run(["less", "LICENSE.md"], check=True)
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
    ...


def the_carcass_version() -> None:
    print(f"Current theCarcass version - {the_carcass_version_string}")


imported_modules = {}  # Global dictionary to store imported modules

def import_modules() -> None:
    """Dynamically imports Python modules from a user-specified directory."""
    
    global imported_modules  # Reference the global variable
    
    # Ask the user for custom directories
    print(f"{PURPLE}[?] Enter the directory where you want to import modules from (leave blank to skip):{RESET}")
    user_dir = input(f"{PURPLE}Directory: {RESET}").strip()

    # Ensure the user provides a valid directory or use default ones
    directories_to_import = []
    
    # Check if the user provided a directory
    if user_dir:
        if os.path.isdir(user_dir):
            directories_to_import.append(user_dir)
            print(f"{GREEN}[+] Importing from user-specified directory: {user_dir}{RESET}")
        else:
            print(f"{RED}[!] Error: '{user_dir}' is not a valid directory.{RESET}")
    
    # Ask the user if they want to import default directories (server_modules and community_modules)
    print(f"{PURPLE}[?] Would you like to import from default directories (server_modules/ and community_modules/) [y/n]?{RESET}")
    use_defaults = input(f"{PURPLE}Use default modules? [y/n]: {RESET}").lower().strip()
    
    if use_defaults == 'y':
        # Add the default directories if confirmed
        current_directory: str = os.path.dirname(__file__)
        directories_to_import.append(os.path.join(current_directory, "server_modules"))
        directories_to_import.append(os.path.join(current_directory, "community_modules"))
        print(f"{GREEN}[+] Importing from default directories: server_modules/, community_modules/{RESET}")
    
    # Import modules from all selected directories
    for directory in directories_to_import:
        try:
            print(f"{GREEN}[+] Importing from {directory}...{RESET}")
            py_files = glob(os.path.join(directory, "*.py"))  # List Python files
            if py_files:
                print(f"{GREEN}[+] Found {len(py_files)} Python files in {directory}.{RESET}")
            for py_file in py_files:
                module_name = os.path.splitext(os.path.basename(py_file))[0]  # Get module name
                print(f"{BLUE}[+] Trying to import module: {module_name}{RESET}")  # Debugging print
                spec = importlib.util.spec_from_file_location(module_name, py_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                imported_modules[module_name] = module  # Store the module in the dictionary
                print(f"{GREEN}[+] Successfully imported module: {module_name}{RESET}")
            if not py_files:
                print(f"{YELLOW}[-] No Python files found in {directory}.{RESET}")
        except Exception as e:
            print(f"{RED}[!] Error importing from directory '{directory}': {e}{RESET}")


def list_imported_modules(show_docs: bool = True) -> None:
    """Lists modules imported from user-specified directories and default directories."""
    
    # Start with a list of the dynamically imported modules
    modules_text = "Imported Modules\n"
    
    if not imported_modules:
        modules_text = "No modules imported yet."
    else:
        for module_name, module in imported_modules.items():
            modules_text += f"\n-> {module_name}:"
            
            if show_docs and module.__doc__:
                modules_text += f"\n{module.__doc__.strip()}"
    
    print(modules_text)  # Use print to show the modules in the console


def the_carcass(tsf_version_string: str, tc_version_string: str) -> None:
    print(f"+{'-' * 16} Welcome to theSuffocater {'-' * 16}+\n")
    print(f" Current tSF version - {tsf_version_string}")
    print(f" Current tC version - {tc_version_string}")
    print(f"+{'-' * 58}+")

    default_modules: dict = {
            "exit": final_exit,
            "clear": tum.clear_screen,
            "help": the_suffocater_help,
            "import": import_modules,
            "modules": list_imported_modules,
            "neofetch": the_suffocater_neofetch,
            "license": the_suffocater_license,
            "changelog": the_suffocater_changelog,
            "documentation": the_suffocater_documentation,
            "tsf_version": the_suffocater_version,
            "tc_version": the_carcass_version
    }

    while True:
        try:
            input_module: str = input(f"{PURPLE}\n(root){RESET} -> # ").lower().strip()
            if input_module.startswith("modules -d"):
                list_imported_modules(show_docs=True)
            elif input_module == "modules":
                list_imported_modules(show_docs=False)
            elif input_module in default_modules:
                default_modules[input_module]()
            elif input_module in globals():
                program = globals()[input_module]
                function_name = input_module
                if hasattr(program, function_name):
                    function = getattr(program, function_name)
                    function()
                else:
                    print(f"{RED}[!] Error: Module '{module}' does not have a function '{function_name}'.{RESET}")
            else:
                print(f"{RED}[!] Error: Module not found.")
                print(f"Please check the name or ensure it is imported and try 'help'.{RESET}")

        except KeyboardInterrupt:
            final_exit()


if __name__ == "__main__":
    try:
        import os
        import sys
        from glob import glob
        import importlib.util
        import the_unix_manager as tum
        from subprocess import run, CalledProcessError
        from the_unix_manager import GREEN, RED, PURPLE, BLACK, WHITE, YELLOW, ORANGE, BLUE, RESET
    except ModuleNotFoundError as import_error:
        print(f"[!] Error: Modules not found. Broken installation?\n\n{import_error}")
        sys.exit(1)
    finally:
        print(f"{GREEN}[*] Modules are successfully imported. Loading theSuffocater global variables...{RESET}")
        
        imported_modules = {}  # Global dictionary to store imported modules
        distros: int = 52
        the_suffocater_contributors: float = 3.5
        with open("tsf_version.txt", "r") as tsf_version_file:
            the_suffocater_version_string: str = tsf_version_file.read().strip()
        with open("tc_version.txt", "r") as tc_version_file:
            the_carcass_version_string: str = tc_version_file.read().strip()

        print(f"{GREEN}[*] Variables are successfully initialized. Loading main function...{RESET}")
        tum.clear_screen()
        the_carcass(tsf_version_string=the_suffocater_version_string, tc_version_string=the_carcass_version_string)
