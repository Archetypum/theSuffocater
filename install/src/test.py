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
    from tkinter import messagebox, scrolledtext, simpledialog, PhotoImage
    from the_unix_manager import GREEN, RED, PURPLE, BLACK, WHITE, YELLOW, ORANGE, BLUE, RESET
except ModuleNotFoundError as import_error:
    print(f"[!] Error: Modules not found. Broken installation?\n\n{import_error}")
    sys.exit(1)
finally:
    print(f"{GREEN}[*] Python modules are successfully imported. Loading theSuffocater global variables...{RESET}")

try:
    icon_path: str = "/etc/tsf/media/thesuffocater_logo.png"
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
    root.quit()


def import_modules() -> None:
    ...


def list_imported_modules(show_docs: bool = False) -> None:
    ...


def get_markdown(document: str = None) -> None:
    ...


def get_version(component: str = None) -> None:
    ...


def import_modules_from_config() -> None:
    ...


if __name__ == "__main__":
    import_modules_from_config()

    root = tk.Tk()
    root.title("theSuffocater")
    root.geometry("800x500")
    root.config(bg="grey24")

    try:
        icon = PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
    except FileNotFoundError:
        messagebox.showerror("[!]", "Error: Can't find the icon.")

    top_frame = tk.Frame(root, bg="grey29")
    top_frame.pack(side="top", fill="x")

    left_frame = tk.Frame(root, width=190, bg="grey20")
    left_frame.pack(side="left", fill="y")

    right_frame = tk.Frame(root, width=130, bg="grey20")
    right_frame.pack(side="right", fill="y")

    # tk.Button(top_frame, text="Import modules", width=20, command=import_modules,  bg="grey24", fg="white").pack(side="left", fill="x", padx=5, pady=5)
    exit_button = tk.Button(top_frame, text="Exit", width=3, bg="grey20", fg="white", activeforeground="red", command=final_exit).pack(side="right", padx=5, pady=5)
    # tk.Button(right_frame, text="list", width=20, command=list).pack(side="top",padx=5, pady=5)
    # tk.Button(right_frame, text="Version", width=20, command=version).pack(side="top",padx=5, pady=5)
    # tk.Button(right_frame, text="Documentation", width=20, command=documentation).pack(side="top",padx=5, pady=5)
    # tk.Button(right_frame, text="License", width=20, command=license).pack(side="top",padx=5, pady=5)
    # tk.Button(right_frame, text="Changelog", width=20, command=changelog).pack(side="top",padx=5, pady=5)

    root.mainloop()
