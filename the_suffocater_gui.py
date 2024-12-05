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
    # Here we importing are python modules, and the most importantly,
    # we are importing "usr.py" - module with all possible functions,
    # widely used by theSuffocater modules.
    # Also here are additional tkinter functions for the graphical interface.
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

# Finds paths to directories where executable files are located.
current_dir: str = os.path.dirname(__file__)
modules_dir: str = os.path.join(current_dir, "modules")
bash_scripts_dir: str = os.path.join(current_dir, "scripts")
py_files = glob.glob(os.path.join(modules_dir, "*.py"))
bash_scripts = glob.glob(os.path.join(bash_scripts_dir, "*.sh"))
bash_scripts_names: list = [os.path.basename(script) for script in bash_scripts]
sys.path.append(modules_dir)

# Imports them.
for py_file in py_files:
    module_name = os.path.splitext(os.path.basename(py_file))[0]
    spec = importlib.util.spec_from_file_location(module_name, py_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals()[module_name] = module


# TODO: Adapt some functions for the GUI.
def run_bash_script(script_name: str) -> None:
    script_path: str = os.path.join(bash_scripts_dir, script_name)
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
    modules_text = "Imported Modules\n"
    for python_file in py_files:
        module_name: str = os.path.splitext(os.path.basename(python_file))[0]
        module = globals().get(module_name)

        if module:
            modules_text += f"\n-> {module_name}:"

            if show_docs and module.__doc__:
                modules_text += f"\n{module.__doc__.strip()}"

    messagebox.showinfo("Modules", modules_text)


def show_scripts() -> None:
    scripts_text = "Available Scripts\n"
    for script_file in bash_scripts:
        script_name: str = os.path.basename(script_file)
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


# Configure command input into the line.
def execute_command(command: str) -> None:
    command = command.lower()
    if command == "exit":
        root.quit()
    elif command == "clear":
        clear_screen()
    elif command == "help":
        show_help()
    elif command == "version":
        show_version("8.2.3-unstable")
    elif command == "modules":
        show_modules()
    elif command == "scripts":
        show_scripts()
    elif command == "documentation":
        show_documentation()
    elif command == "license":
        show_license()
    elif command == "changelog":
        show_changelog()
    else:
        messagebox.showerror("[!] Error", f"Unknown command: {command}")


# The main graphic part with frames and buttons.
def main_gui(suffocater_version: str) -> None:
    global root
    root = tk.Tk()
    root.title("theSuffocater GUI")
    root.geometry("700x500")
    root.config(bg="grey24")

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

    def execute_gui_command(event) -> None:
        command = command_entry.get()
        execute_command(command)
        command_entry.delete(0, tk.END)

    top_frame = tk.Frame(root, bg="grey29")
    top_frame.pack(side="top", fill="x")
    
    left_frame = tk.Frame(root, width=170, bg="grey20")
    left_frame.pack(side="left", fill="y")

    tk.Button(top_frame, text="Modules", width=30, command=on_modules,  bg='grey24', fg='white', activeforeground="green3").pack(side="left", padx=5, pady=5)
    tk.Button(top_frame, text="Exit", width=3, bg="grey20", fg='white', activeforeground="red", command=exit_app).pack(side="right", padx=5, pady=5)
    
    tk.Button(left_frame, text="Help", width=20, command=on_help).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Version", width=20, command=on_version).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Scripts", width=20, command=on_scripts).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Clear Screen", width=20, command=on_clear).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Documentation", width=20, command=on_documentation).pack(padx=5, pady=5)
    tk.Button(left_frame, text="License", width=20, command=on_license).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Changelog", width=20, command=on_changelog).pack(padx=5, pady=5)

    output_text = tk.Text(root, height=15, width=50, bg="grey20", state=tk.DISABLED)
    output_text.pack(pady=10)

    command_entry = tk.Entry(root, width=53, bg="grey20")
    command_entry.pack(pady=5)
    command_entry.bind("<Return>", execute_gui_command)

    root.mainloop()


if __name__ == "__main__":
    suffocater_version: str = "8.2.3-unstable"
    main_gui(suffocater_version)
