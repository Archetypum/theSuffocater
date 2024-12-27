#!/usr/bin/python3
#
# This thing is called the "Carcass" - the heart of theSuffocater.
# Carcass destiny is to load modules located in the thesuffocater/modules
# for further using.
# 
# Usually carcass don't receive many updates because it's already serving
# its functionality very good.
# 
# Graphical frontend - the_suffocater_gui.py

suffocater_version: str = "v1.0.1-unstable       "
neofetch: str = f"""
  GOLOGOLOGOLOGOLO      theSuffocater version - {suffocater_version}
 OGOLOGOLOGOLOGOLOG
LOGOLOGOLOGOLOGOLOGO
LOGOLOGOLOGOLOGOLOGO
LOGOLOGOLOGOLOGOLOGO
LOGOLOGOLOGOLOGOLOGO
LOGOLOGOLOGOLOGOLOGO
 OGOLOGOLOGOLOGOLOG
  GOLOGOLOGOLOGOLO
"""

try:
    # Here we are importing are python modules, and the most importantly,
    # we are importing "usr.py" - module with all possible functions,
    # widely used by theSuffocater modules.
    import os
    import sys
    modules_dir: str = os.path.join(os.path.dirname(__file__), "modules")
    sys.path.append(modules_dir)
    import usr
    import glob
    import subprocess
    import importlib.util
    from usr import GREEN, RED, PURPLE, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")
    sys.exit(1)


def final_exit() -> None:
    """Exits theSuffocater."""
    sys.exit(0)


def clear_screen() -> None:
    """Clears the screen."""
    os.system("clear")


def the_suffocater_help() -> None:
    """Displays help message."""
    print("\nCommands:")
    print(" exit - exit theSuffocater.")
    print(" clear - clear screen.")
    print(" help - this message.")
    print(" modules [-d] - list imported modules (use -d to include documentation).")
    print(" scripts - list available bash scripts")
    print(" version - current version of theSuffocater.")
    print(" documentation - ultimate guide to theSuffocater.")
    print(" license - check the license.")
    print(" changelog - check whats new in this version.")
    print(f"\nFor more info, check 'documentation'.")


def the_suffocater_neofetch(suffocater_version: str) -> str:
    """Displays brief statistic about theSuffocater."""
    return f"{neofetch}"


def the_suffocater_version(suffocater_version: str) -> str:
    """Returns current theSuffocater version string."""
    return f"Current version - {suffocater_version}"


def the_suffocater_documentation() -> None:
    """
    In normal scenario, opens 'README.md' so the user can read brief documentation.
    Otherwise, tells user about broken installation.
    """
    try:
        os.system("less README.md")
    except FileNotFoundError:
        print(f"{RED}[!] Error: README.md file not found.\nBroken installation?{RESET}")


def the_suffocater_license() -> None:
    """
    In normal scenario, opens 'LICENSE.md' so the user can check theSuffocater license - GNU GPLv3.
    Otherwise, tells user about broken installation.
    """ 
    try:
        os.system("less LICENSE.md")
    except FileNotFoundError:
        print(f"{RED}[!] Error: LICENSE.md file not found.\nBroken installation?{RESET}")


def the_suffocater_changelog() -> None:
    """
    In normal scenario, opens CHANGELOG.md file so user can check details about the release.
    Otherwise, tells user about broken installation.
    """
    try:
        os.system("less CHANGELOG.md")
    except FileNotFoundError:
        print(f"{RED}[!] Error: CHANGELOG.md file not found.\nBroken installation?{RESET}")


def list_imported_modules(show_docs: bool = True) -> None:
    """
    Lists modules imported from 'modules/' directory.
    '-d' argument shows documentation alongside the modules.
    """
    print("+-------------------- Imported Modules --------------------+")
    for py_file in py_files:
        module_name: str = os.path.splitext(os.path.basename(py_file))[0]
        module = globals().get(module_name)

        if module:
            print(f"-> {module_name}:")

            if show_docs and module.__doc__:
                print(module.__doc__.strip())


def list_available_scripts() -> None:
    """
    Lists shell scripts from 'scripts/' directory.
    """
    print("+-------------------- Available Scripts -------------------+")
    for script_file in bash_scripts:
        script_name: str = os.path.basename(script_file)
        print(f"-> {script_name}")


def run_bash_script(script_name: str) -> None:
    """Runs shell scripts."""
    script_path: str = os.path.join(bash_scripts_dir, script_name)
    try:
        subprocess.run(["bash", script_path], check=True)
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error running script '{script_name}': {error}{RESET}")


def the_suffocater_main(suffocater_version: str) -> None:
    """
    Main function.
    Provides terminal-like interface to the user and offers
    9 pre-build functions (default_modules dictionary).
    """

    os.system("clear")
    version: str = the_suffocater_version(suffocater_version)
    print(f"+---------------- Welcome to theSuffocater ----------------+")
    print(f"| {version}                 |")

    default_modules: dict = {
        "exit": final_exit,
        "clear": clear_screen,
        "help": the_suffocater_help,
        "modules": lambda: list_imported_modules(show_docs=True),
        "license": the_suffocater_license,
        "scripts": list_available_scripts,
        "neofetch": lambda: print(the_suffocater_neofetch(suffocater_version)),
        "changelog": the_suffocater_changelog,
        "version": lambda: print(the_suffocater_version(suffocater_version)),
        "documentation": the_suffocater_documentation
    }

    while True:
        module: str = input(f"{PURPLE}\n(root){RESET} -> # ").lower().strip()
        if module.startswith("modules -d"):
            list_imported_modules(show_docs=True)
        elif module == "modules":
            list_imported_modules(show_docs=False)
        elif module in default_modules:
            default_modules[module]()
        elif module in globals():
            program = globals()[module]
            function_name = module
            if hasattr(program, function_name):
                function = getattr(program, function_name)
                function()
            else:
                print(f"{RED}[!] Error: Module '{module}' does not have a function '{function_name}'.{RESET}")
        elif module in bash_scripts_names:
            run_bash_script(module)
        else:
            print(f"{RED}[!] Error: Module or script not found.")
            print(f"Please check the name or ensure it is imported and try 'help'.{RESET}")


if __name__ == "__main__":
    # Checks if user is root.
    # Most of theSuffocater modules can't run without root privileges.
    if os.geteuid() == 0:
        current_dir: str = os.path.dirname(__file__)
        modules_dir: str = os.path.join(current_dir, "modules")
        bash_scripts_dir: str = os.path.join(current_dir, "scripts")
        py_files: list = glob.glob(os.path.join(modules_dir, "*.py"))
        bash_scripts: list = glob.glob(os.path.join(bash_scripts_dir, "*.sh"))

        bash_scripts_names: list = [os.path.basename(script) for script in bash_scripts]

        for py_file in py_files:
            module_name: str = os.path.splitext(os.path.basename(py_file))[0]
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module

        the_suffocater_main(suffocater_version)
    else:
        print(f"{RED}[!] Error: Carcass requires root privileges to run certain modules.{RESET}")
        sys.exit(1)
