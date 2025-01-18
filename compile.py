#!/usr/bin/python3

try:
    import os
    import sys
    import subprocess
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: Failed to import: {import_error}{RESET}")


def compile_tsf(output_dir: str = "dist", onefile=True) -> None:
    """
    docstring

    Args:
        output_dir (str):
        onefile (bool)
    """

    if not os.path.exists("src/the_carcass_cli.py"):
        print(f"{RED}[!] Error: Can't find source.{RESET}")
        return

    cli_compile_command: list = ["pyinstaller",
                     "--noconfirm",
                     "--onefile" if onefile else "--onedir",
                     "--distpath", output_dir,
                     "src/the_carcass_cli.py"]
    gui_compile_command: list = ["pyinstaller",
                     "--noconfirm",
                     "--onefile" if onefile else "--onedir",
                     "--distpath", output_dir,
                     "src/the_carcass_cli.py"]

    try:
        print("[<==] Launching PyInstaller...")
        print("[<==] Compiling CLI...")
        subprocess.run(cli_compile_command, check=True)
        if tum.prompt_user("[?] Compile GUI?"):
            subprocess.run(gui_compile_command, check=True)

        print(f"{GREEN}[*] Succesfully compiled!{RESET}")
    except subprocess.CalledProcessError as compile_error:
        print(f"{RED}[!] Error while compiling:\n{compile_error}{RESET}")
    except FileNotFoundError:
        print(f"{RED}[!] Error: 'pyinstaller' is not installed.{RESET}")


if __name__ == "__main__":
    compile_tsf()
