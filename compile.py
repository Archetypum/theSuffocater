#!/usr/bin/python3

try:
    import os
    import sys
    import subprocess
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: Failed to import: {import_error}{RESET}")


def move2etc() -> None:
    """

    """

    if os.path.exists("install/tsf"):
        subprocess.run(["sudo", "cp", "-r", "install/tsf", "/etc/tsf"], check=True)
        print(f"{GREEN}[*] Copying 'install/tsf' to '/etc/tsf'...")


def move2bin() -> None:
    """

    """

    if os.path.exists("the_carcass_cli.spec"):
        subprocess.run(["rm", "the_carcass_cli.spec"], check=True)
        print(f"{GREEN}[*] Removing 'the_carcass_cli.spec'...{RESET}")

    if os.path.exists("install/src/the_carcass_gui.spec"):
        subprocess.run(["rm", "install/src/the_carcass_gui.spec"], check=True)
        print(f"{GREEN}[*] Removing 'the_carcass_gui.spec'...{RESET}")

    if os.path.exists("build"):
        subprocess.run(["rm", "-rf", "build"], check=True)
        print(f"{GREEN}[*] Removing 'build'...{RESET}")

    if os.path.exists("dist"):
        subprocess.run(["sudo", "mv", "dist/the_carcass_cli/the_carcass_cli", "dist/the_carcass_cli/_internal", "/usr/bin/"], check=True)
        print(f"{GREEN}[*] Moving 'the_carcass_cli', '_internal/' to '/usr/bin'...") 
        # if os.path.exists(f"{current_directory}/dist/the_carcass_gui"):
        #    subprocess.run(["mv", f"{current_directory}/dist/the_carcass_gui", "/usr/bin/thesuffocater_gui"], check=True)
    
    subprocess.run(["rm", "-rf", "dist"], check=True)
    move2etc()
    

def compile_tsf() -> None:
    """
    Compiles theCarcass_cli/gui
    """

    if not os.path.exists("install/src/the_carcass_cli.py"):
        print(f"{RED}[!] Error: Can't find source in install/src/.{RESET}")
        return

    cli_compile_command: list = ["pyinstaller",
                     "--noconfirm",
                     "install/src/the_carcass_cli.py"]
    gui_compile_command: list = ["pyinstaller",
                     "--noconfirm",
                     "install/src/the_carcass_gui.py"]

    try:
        print(f"{GREEN}[<==] Launching PyInstaller...{RESET}")
        print(f"{GREEN}[<==] Compiling CLI...\n{RESET}")
        subprocess.run(cli_compile_command, check=True)
        if tum.prompt_user("[?] Compile GUI?"):
            subprocess.run(gui_compile_command, check=True)

        print(f"{GREEN}[*] Succesfully compiled!{RESET}")

        move2bin()
    except subprocess.CalledProcessError as compile_error:
        print(f"{RED}[!] Error while compiling:\n{compile_error}{RESET}")
    except FileNotFoundError:
        print(f"{RED}[!] Error: 'pyinstaller' is not installed.{RESET}")


if __name__ == "__main__":
    compile_tsf()
