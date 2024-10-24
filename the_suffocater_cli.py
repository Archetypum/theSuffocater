#!/usr/bin/python3

import os
import glob
import subprocess
from sys import exit
import importlib.util


def final_exit() -> None:
    exit()


def clear_screen() -> None:
    os.system("clear")


def the_suffocater_help() -> None:
    print("\nCommands:")
    print(" exit - exit theSuffocater.")
    print(" clear - clear screen.")
    print(" help - this message.")
    print(" modules - list imported modules")
    print(" scripts - list available bash scripts")
    print(" version - current version of theSuffocater.")
    print(" documentation - ultimate guide to theSuffocater.")
    print("\nFor more info, check 'documentation'.")


def the_suffocater_version(suffocater_version: str) -> str:
    return f"Current version - {suffocater_version}"


def the_suffocater_documentation() -> None:
    os.system("less README.md")


def list_imported_modules() -> None:
    print("+-------------------- Imported Modules --------------------+")
    for py_file in py_files:
        module_name: str = os.path.splitext(os.path.basename(py_file))[0]
        module = globals().get(module_name)

        if module:
            print(f"\n-> {module_name}:")

            if module.__doc__:
                print(module.__doc__.strip())
            else:
                print("No documentation available for this module.")


def list_available_scripts() -> None:
    print("+-------------------- Available Scripts -------------------+")
    for script_file in bash_scripts:
        script_name: str = os.path.basename(script_file)
        print(f"-> {script_name}")


def run_bash_script(script_name: str) -> None:
    script_path = os.path.join(bash_scripts_dir, script_name)
    try:
        subprocess.run(["bash", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running script '{script_name}': {e}")


def the_suffocater_main(suffocater_version: str) -> None:
    os.system("clear")
    version = the_suffocater_version(suffocater_version)
    print(f"+---------------- Welcome to theSuffocater ----------------+")
    print(f"| {version}                   |")

    default_modules: dict = {
        "exit": final_exit,
        "clear": clear_screen,
        "help": the_suffocater_help,
        "modules": list_imported_modules,
        "scripts": list_available_scripts,
        "version": lambda: print(the_suffocater_version(suffocater_version)),
        "documentation": the_suffocater_documentation,
    }

    while True:
        module: str = input("\n# ")
        if module in default_modules:
            default_modules[module]()
        elif module in globals():
            program = globals()[module]
            function_name = module
            if hasattr(program, function_name):
                function = getattr(program, function_name)
                function()
            else:
                print(f"Error: Module '{module}' does not have a function '{function_name}'.")
        elif module in bash_scripts_names:
            run_bash_script(module)
        else:
            print("Error: Module or script not found. Please check the name or ensure it is imported and try 'help'.")


if __name__ == "__main__":
    if os.geteuid() == 0:
        current_dir: str = os.path.dirname(__file__)
        modules_dir: str = os.path.join(current_dir, "modules")
        bash_scripts_dir: str = os.path.join(current_dir, "scripts")  # Directory for bash scripts
        py_files: list = glob.glob(os.path.join(modules_dir, "*.py"))
        bash_scripts: list = glob.glob(os.path.join(bash_scripts_dir, "*.sh"))  # Load bash scripts

        bash_scripts_names = [os.path.basename(script) for script in bash_scripts]

        for py_file in py_files:
            module_name: str = os.path.splitext(os.path.basename(py_file))[0]
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module

        suffocater_version: str = "7.0.0-testing        "
        the_suffocater_main(suffocater_version)
    else:
        print("This code requires root privileges to run certain modules.")
        exit()
