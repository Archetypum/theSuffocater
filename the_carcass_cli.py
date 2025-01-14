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
    print(f"""    
{BLUE}               
                 __________           {RESET}theSuffocater version - {GREEN}{the_suffocater_version_string}{BLUE}      
                [0000000000]          
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


def import_modules() -> None:
    current_directory: str = os.path.dirname(__file__)

    print("\nDefault module directories:")
    print(f" {BLUE}server_modules{RESET} ({GREEN}already imported{RESET}) - essential server modules.")
    print(f" {PURPLE}community_modules{RESET} - quality of life modules.")

    import_directory_path: str = input("\n[==>] Enter directory path: ").lower()
    if import_directory_path == "server_modules":
        print(f"{GREEN}[*] Already imported.{RESET}")
    elif import_directory_path == "community_modules":
        server_modules_directory: str = os.path.join(current_directory, "community_modules")
        python_files: list = glob(os.path.join(server_modules_directory, "*.py"))
        for python_file in python_files:
            module_name: str = os.path.splitext(os.path.basename(python_file))[0]
            spec = importlib.util.spec_from_file_location(module_name, python_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module

            print(f"[<==] Importing {module_name}...")
    

def list_imported_modules(show_docs: bool = True) -> None:
    print(f"+{'-' * 20} Imported modules {'-' * 20}+")
    for python_file in python_files:
        module_name: str = os.path.splitext(os.path.basename(python_file))[0]
        module = globals().get(module_name)

        if module:
            print(f"-> {module_name}")

            if show_docs and module.__doc__:
                print(module.__doc__.strip())
 

def the_carcass(tsf_version_string: str, tc_version_string: str) -> None:
    print(f"+{'-' * 16} Welcome to theSuffocater {'-' * 16}+\n")
    print(f" Current tSF version - {tsf_version_string}")
    print(f" Current tC version - {tc_version_string}\n")
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
            print("\n")
            final_exit()


try:
    print(f"[==>] Importing python modules...")
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
    print(f"{GREEN}[*] Python modules are successfully imported. Loading theSuffocater global variables...{RESET}")
    
try:
    distros_count: int = 52
    the_suffocater_contributors: float = 3.5
    current_directory: str = os.path.dirname(__file__)
    with open("tsf_version.txt", "r") as tsf_version_file:
        the_suffocater_version_string: str = tsf_version_file.read().strip()
    with open("tc_version.txt", "r") as tc_version_file:
        the_carcass_version_string: str = tc_version_file.read().strip()
except FileNotFoundError as variable_error:
    print(f"{RED}[!] Error: Failed to create global variables:\n\n{variable_error}{RESET}")
    sys.exit(1)
finally:
    print(f"{GREEN}[*] Variables are successfully initialized. Loading modules from 'server_modules/'...{RESET}")

server_modules_directory: str = os.path.join(current_directory, "server_modules")
python_files: list = glob(os.path.join(server_modules_directory, "*.py"))
for python_file in python_files:
    module_name: str = os.path.splitext(os.path.basename(python_file))[0]
    spec = importlib.util.spec_from_file_location(module_name, python_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals()[module_name] = module
    print(f"[<==] Importing {module_name}...")

print(f"{GREEN}[*] Successfully imported modules. Loading main function...{RESET}")

if __name__ == "__main__":
    tum.clear_screen()
    the_carcass(tsf_version_string=the_suffocater_version_string, tc_version_string=the_carcass_version_string)
