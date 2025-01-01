#!/usr/bin/python3
#
# This thing is called the "theCarcass" - the heart of theSuffocater.
# theCarcass destiny is to load modules located in the thesuffocater/modules
# for further using.
# 
# Usually theCarcass don't receive many updates because it's already serving
# its functionality very good.
#
# This is a graphical frontend, normal cli version is 'the_suffocater_cli.py'.

try:
    # Here we are importing are python modules, and the most importantly,
    # we are importing "the_unix_manager.py" - module with all possible functions,
    # widely used by theSuffocater modules.
    # Also, here are additional tkinter functions for the graphical interface.
    import os
    import sys
    modules_dir = os.path.join(os.path.dirname(__file__), "modules")
    sys.path.append(modules_dir)
    import glob
    import subprocess
    import tkinter as tk
    import importlib.util
    import the_unix_manager as tum
    from the_unix_manager import RED, RESET
    from tkinter import messagebox, PhotoImage
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")
    sys.exit(1)


def run_bash_script(script_name: str) -> None:
    """Runs shell scripts."""
    script_path: str = os.path.join(bash_scripts_dir, script_name)
    try:
        subprocess.run(["bash", script_path], check=True)
        messagebox.showinfo("[*] Success", f"Script {script_name} executed successfully.")
    except subprocess.CalledProcessError as error:
        messagebox.showerror("[!] Error", f"Error running script '{script_name}': {error}")


def final_exit() -> None:
    """Exits theSuffocater."""
    root.quit()


def the_suffocater_version(suffocater_version: str) -> None:
    """Returns current theSuffocater version string."""
    messagebox.showinfo("Version", f"Current version - {suffocater_version}")


def the_suffocater_help() -> None:
    """Displays help message."""
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
    """Clears the screen."""
    os.system("clear")


def list_imported_modules(show_docs: bool = False) -> None:
    """
    Lists modules imported from 'modules/' directory.
    '-d' argument shows documentation alongside the modules.
    """
    modules_text: str = "Imported Modules\n"
    for python_file in py_files:
        module_name: str = os.path.splitext(os.path.basename(python_file))[0]
        module = globals().get(module_name)

        if module:
            modules_text += f"\n-> {module_name}:"

            if show_docs and module.__doc__:
                modules_text += f"\n{module.__doc__.strip()}"

    messagebox.showinfo("Modules", modules_text)


def list_available_scripts() -> None:
    """
    Lists shell scripts from 'scripts/' directory.
    """
    scripts_text: str = "Available Scripts\n"
    for script_file in bash_scripts:
        script_name: str = os.path.basename(script_file)
        scripts_text += f"-> {script_name}\n"
    messagebox.showinfo("Scripts", scripts_text)


def the_suffocater_documentation() -> None:
    """
    In normal scenario, opens 'README.md' so the user can read brief documentation.
    Otherwise, tells user about broken installation.
        """
    try:
        os.system("less README.md")
    except FileNotFoundError:
        messagebox.showerror("Error", "README.md file not found.\nBroken installation?")


def the_suffocater_license() -> None:
    """
    In normal scenario, opens 'LICENSE.md' so the user can check theSuffocater license - GNU GPLv3.
    Otherwise, tells user about broken installation.
    """
    try:
        os.system("less LICENSE.md")
    except FileNotFoundError:
        messagebox.showerror("[!] Error", "LICENSE.md file not found.\nBroken installation?")


def the_suffocater_changelog() -> None:
    """
    In normal scenario, opens CHANGELOG.md file so user can check details about the release.
    Otherwise, tells user about broken installation.
    """
    try:
        os.system("less CHANGELOG.md")
    except FileNotFoundError:
        messagebox.showerror("[!] Error", "CHANGELOG.md file not found.\nBroken installation?")


def execute_command(command: str) -> None:
    """Executes GUI commands."""
    default_modules: dict = {
            "exit": final_exit,
            "clear": clear_screen,
            "help": the_suffocater_help,
            "modules": lambda: list_imported_modules(show_docs=True),
            "license": the_suffocater_license,
            "scripts": list_available_scripts,
            "changelog": the_suffocater_changelog,
            "version": lambda: print(the_suffocater_version(suffocater_version)),
            "documentation": the_suffocater_documentation
            }

    command: str = command.lower()
    if command.startswith("modules -d"):
        list_imported_modules(show_docs=True)
    elif command == "modules":
        list_imported_modules(show_docs=False)
    elif command in default_modules:
        default_modules[command]()
    elif command in globals():
        program = globals()[command]
        function_name = command
        if hasattr(program, function_name):
            function = getattr(program, function_name)
            function()
        else:
            print(f"[!] Error: Module '{module}' does not have a function '{function_name}'.")
    elif command in bash_scripts_names:
        run_bash_script(command)
    else:
        print("[!] Error: Module or script not found.")
        print("Please check the name or ensure it is imported and try 'help'.")


def main_gui(suffocater_version: str) -> None:
    """
    Main function.
    Provides graphical user interface to the user and offers
    9 pre-build functions (default_modules dictionary).
    """
    global root
    root = tk.Tk()
    root.title("theSuffocater GUI")
    root.geometry("700x500")
    root.config(bg="grey24")
    icon = PhotoImage(file="logo.png")
    root.iconphoto(False, icon)

    def exit_app() -> None:
        final_exit()

    def on_help() -> None:
        the_suffocater_help()

    def on_version() -> None:
        the_suffocater_version(suffocater_version)

    def on_modules() -> None:
        list_imported_modules()

    def on_scripts() -> None:
        list_available_scripts()

    def on_clear() -> None:
        clear_screen()

    def on_documentation() -> None:
        the_suffocater_documentation()

    def on_license() -> None:
        the_suffocater_license()

    def on_changelog() -> None:
        the_suffocater_changelog()

    def execute_gui_command(event) -> None:
        command: str = command_entry.get()
        execute_command(command)
        command_entry.delete(0, tk.END)

    top_frame = tk.Frame(root, bg="grey29")
    top_frame.pack(side="top", fill="x")
    
    left_frame = tk.Frame(root, width=170, bg="grey20")
    left_frame.pack(side="left", fill="y")

    tk.Button(top_frame, text="Modules", width=30, command=on_modules,  bg="grey24", fg="white", activeforeground="green3").pack(side="left", padx=5, pady=5)
    tk.Button(top_frame, text="Exit", width=3, bg="grey20", fg="white", activeforeground="red", command=exit_app).pack(side="right", padx=5, pady=5)
    tk.Button(left_frame, text="Help", width=20, command=on_help).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Version", width=20, command=on_version).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Scripts", width=20, command=on_scripts).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Clear Screen", width=20, command=on_clear).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Documentation", width=20, command=on_documentation).pack(padx=5, pady=5)
    tk.Button(left_frame, text="License", width=20, command=on_license).pack(padx=5, pady=5)
    tk.Button(left_frame, text="Changelog", width=20, command=on_changelog).pack(padx=5, pady=5)

    output_text = tk.Text(root, height=15, width=50, bg="grey20", fg='white', state=tk.DISABLED)
    output_text.pack(pady=10, expand=True, fill=tk.BOTH)

    command_entry = tk.Entry(root, bg="grey20", fg='white')
    command_entry.pack(pady=5, expand=False, fill=tk.X)
    command_entry.bind("<Return>", execute_gui_command)

    root.mainloop()


if __name__ == "__main__":
    if os.geteuid() == 0:
        # Checks if user is root.
        # Most of theSuffocater modules can't run without root privileges.
        current_dir: str = os.path.dirname(__file__)
        modules_dir: str = os.path.join(current_dir, "modules")
        bash_scripts_dir: str = os.path.join(current_dir, "scripts")
        py_files: list = glob.glob(os.path.join(modules_dir, "*.py"))
        bash_scripts: list = glob.glob(os.path.join(bash_scripts_dir, "*.sh"))
        bash_scripts_names: list = [os.path.basename(script) for script in bash_scripts]
        sys.path.append(modules_dir)

        for py_file in py_files:
            module_name = os.path.splitext(os.path.basename(py_file))[0]
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            globals()[module_name] = module
    else:
        print(f"{RED}[!] Error: Carcass requires root privileges to run certain modules.{RESET}")
        sys.exit(1)

    suffocater_version: str = "1.0.0-stable"
    main_gui(suffocater_version)
