#!/usr/bin/python3

#
# This thing is called the "Carcass" - the heart of theSuffocater.
# Carcass destiny is to load modules located in the /fear-the-suffocater/modules
# for further using.
# 
# Usually carcass don't receive many updates because it's already serving
# its functionality very good.
# 
# This is a graphical frontend, normal cli version is 'the_suffocater_gui.py'.

try:
    import os
    import sys
    modules_dir = os.path.join(os.path.dirname(__file__), "modules")
    sys.path.append(modules_dir)
    import usr
    import glob
    import subprocess
    import tkinter as tk
    import importlib.util
    from tkinter import messagebox
    from usr import RED, GREEN, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: module not found:\n{error}{RESET}")
    sys.exit(1)

current_dir = os.path.dirname(__file__)
modules_dir = os.path.join(current_dir, "modules")
bash_scripts_dir = os.path.join(current_dir, "scripts")
py_files = glob.glob(os.path.join(modules_dir, "*.py"))
bash_scripts = glob.glob(os.path.join(bash_scripts_dir, "*.sh"))
bash_scripts_names = [os.path.basename(script) for script in bash_scripts]
sys.path.append(modules_dir)

for py_file in py_files:
    module_name = os.path.splitext(os.path.basename(py_file))[0]
    spec = importlib.util.spec_from_file_location(module_name, py_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals()[module_name] = module

def run_bash_script(script_name: str) -> None:
    script_path = os.path.join(bash_scripts_dir, script_name)
    try:
        subprocess.run(["bash", script_path], check=True)
        messagebox.showinfo("[*] Success", f"Script {script_name} executed successfully.")
    except subprocess.CalledProcessError as error:
        messagebox.showerror("[!] Error", f"Error running script '{script_name}': {error}")


def show_version(suffocater_version: str) -> None:
    messagebox.showinfo("Version", f"Current version - {suffocater_version}")


def show_help() -> None:
    help_text: str = (
        "Commands:\n"
        "exit - exit theSuffocater.\n"
        "clear - clear screen.\n"
        "help - this message.\n"
        "modules [-d] - list imported modules (use -d to include documentation).\n"
        "scripts - list available bash scripts\n"
        "version - current version of theSuffocater.\n"
        "documentation - ultimate guide to theSuffocater.\n"
        "license - check the license.\n"
        "changelog - check what's new in this version."
    )
    messagebox.showinfo("Help", help_text)


def clear_screen() -> None:
    os.system("clear")


def show_modules(show_docs: bool = False) -> None:
    modules_text = "+-------------------- Imported Modules --------------------+\n"
    for python_file in py_files:
        module_name = os.path.splitext(os.path.basename(python_file))[0]
        module = globals().get(module_name)

        if module:
            modules_text += f"\n-> {module_name}:"

            if show_docs and module.doc:
                modules_text += f"\n{module.doc.strip()}"

        messagebox.showinfo("Modules", modules_text)


def show_scripts() -> None:
    scripts_text = "+-------------------- Available Scripts -------------------+\n"
    for script_file in bash_scripts:
        script_name = os.path.basename(script_file)
        scripts_text += f"-> {script_name}\n"
    messagebox.showinfo("Scripts", scripts_text)


def show_documentation() -> None:
    try:
        os.system("less README.md")
    except FileNotFoundError:
        messagebox.showerror("Error", "README.md file not found.\nBroken installation?")


def show_license() -> None:
    try:
        os.system("less LICENSE.md")
    except FileNotFoundError:
        messagebox.showerror("[!] Error", "LICENSE.md file not found.\nBroken installation?")


def show_changelog() -> None:
    try:
        os.system("less CHANGELOG.md")
    except FileNotFoundError:
        messagebox.showerror("[!] Error", "CHANGELOG.md file not found.\nBroken installation?")


def main_gui(suffocater_version: str) -> None:
    root = tk.Tk()
    root.title("theSuffocater GUI")
    root.geometry("400x300")
    root.config(bg="#696969")

    def exit_app() -> None:
        root.quit()

    def on_help() -> None:
        show_help()

    def on_version() -> None:
        show_version(suffocater_version)

    def on_modules() -> None:
        show_modules()

    def on_scripts() -> None:
        show_scripts()

    def on_clear() -> None:
        clear_screen()

    def on_documentation() -> None:
        show_documentation()

    def on_license() -> None:
        show_license()

    def on_changelog() -> None:
        show_changelog()

    tk.Button(root, text="Exit", command=exit_app).pack(pady=5)
    tk.Button(root, text="Help", command=on_help).pack(pady=5)
    tk.Button(root, text="Version", command=on_version).pack(pady=5)
    tk.Button(root, text="Modules", command=on_modules).pack(pady=5)
    tk.Button(root, text="Scripts", command=on_scripts).pack(pady=5)
    tk.Button(root, text="Clear Screen", command=on_clear).pack(pady=5)
    tk.Button(root, text="Documentation", command=on_documentation).pack(pady=5)
    tk.Button(root, text="License", command=on_license).pack(pady=5)
    tk.Button(root, text="Changelog", command=on_changelog).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    suffocater_version: str = "8.2.2-unstable"
    main_gui(suffocater_version)
