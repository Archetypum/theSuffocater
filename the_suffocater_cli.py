#!/usr/bin/python3

import os
import glob
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
        else:
            print("Error: Module not found. Please check the name or ensure it is imported and try 'help'.")


if __name__ == "__main__":
    if os.geteuid() == 0:
        current_dir: str = os.path.dirname(__file__)
        modules_dir: str = os.path.join(current_dir, "modules")
        py_files: list = glob.glob(os.path.join(modules_dir, "*.py"))

        for py_file in py_files:
            module_name: str = os.path.splitext(os.path.basename(py_file))[0]
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module

        suffocater_version: str = "6.2.2-stable        "
        the_suffocater_main(suffocater_version)
    else:
        print("This code requires root privilges to run certain modules.")
        exit()
