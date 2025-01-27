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
    from tkinter import messagebox
    from tkinter import scrolledtext
    from tkinter import simpledialog
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


def final_exit(root) -> None:
    root.quit()


def the_global_version(root) -> None:
    messagebox.showinfo("version", f"Current theSuffocater version - {the_suffocater_version_string} \nCurrent theCarcass version - {the_carcass_version_string}")


def the_suffocater_license(root) -> None:
    try:
        run(["less", "LICENSE-GPL.md"], check=True)
    except (FileNotFoundError, CalledProcessError):
        print(f"{RED}[!] Error: 'LICENSE.md' file not found. Broken installation?")


def the_suffocater_changelog(root) -> None:
    try:
        run(["less", "CHANGELOG.md"], check=True)
    except (FileNotFoundError, CalledProcessError):
        print(f"{RED}[!] Error: 'CHANGELOG.md' file not found. Broken installation?")


def the_suffocater_documentation(root) -> None:
    try:
        run(["less", "README.md"], check=True)
    except (FileNotFoundError, CalledProcessError):
        print(f"{RED}[!] Error: 'README.md' file not found. Broken installation?")

    try:
        if "GNOME" in os.environ.get("XDG_CURRENT_DESKTOP", ""):
            subprocess.run(["gnome-terminal", "--", "bash", "-c", "cat README.md; exec bash"], check=True)
        elif "KDE" in os.environ.get("XDG_CURRENT_DESKTOP", ""):
            subprocess.run(["konsole", "-e", "bash", "-c", "cat README.md; exec bash"], check=True)
        elif "XFCE" in os.environ.get("XDG_CURRENT_DESKTOP", ""):
            subprocess.run(["xfce4-terminal", "-e", "bash -c 'cat README.md; exec bash'"], check=True)
        else:
            messagebox.showerror(f"{RED}[!] Error: 'README.md' file not found. Broken installation?{RESET}")
    except (FileNotFoundError, CalledProcessError):
        messagebox.showerror(f"{RED}[!] Error: Could not open terminal.{RESET}")          


def import_modules(root, left_frame) -> None:
    directory_path = simpledialog.askstring("Enter modules directory path (e.g /home/$USER/Desktop/my_python_modules)", "[==>] ", parent=root)
    if not os.path.isdir(directory_path):
        messagebox.showerror(f"{RED}[!] Error: Not a directory.{RESET}", parent=root)
    
    import_functions_from_directory(root, directory_path)
    create_module_buttons(root, left_frame)


def list_imported_modules(root, show_docs: bool = False) -> None:
    info_window = tk.Toplevel(root)
    info_window.title("Imported Modules")

    text_area = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, width=50, height=20)
    text_area.pack(padx=10, pady=10)

    output = f"+{'-' * 15} Imported modules {'-' * 15}+\n"
    for module_path, module_info in loaded_modules.items():
        output += f"\n  -> Path: {module_path}\n"
        if show_docs:
            output += f"  -> Docstring: {module_info['docstring'] or 'None'}\n"
        output += "  --> Functions:\n"
        for func_name, func_docstring in module_info["functions"].items():
            if show_docs:
                output += f"    - {func_name}: {func_docstring or 'None'}\n"
            else:
                output += f"    - {func_name}\n"

    text_area.insert(tk.END, output)
    text_area.config(state=tk.DISABLED)

    ok_button = tk.Button(info_window, text="ok", command=info_window.destroy)
    ok_button.pack(pady=10)                    


def import_functions_from_directory(root, directory_path: str) -> None:
    for filename in os.listdir(directory_path):
        if filename.endswith(".py"):
            file_path: str = os.path.join(directory_path, filename)
            try:
                module_name = filename[:-3]
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if file_path in loaded_modules:
                    del loaded_modules[file_path]
                    
                loaded_modules[file_path] = {
                    "docstring": module.__doc__,
                    "functions": {}
                }
                
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj):
                       loaded_modules[file_path]["functions"][name] = obj.__doc__
                       default_modules[name] = obj

            except FileNotFoundError as module_import_error:
                messagebox.showerror(f"{RED}[!] Error: Can't import module from {file_path}:\n{module_import_error}{RESET}", parent=root)


def show_module_info(root, left_frame, module_name: str) -> None:
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != left_frame:
            widget.destroy()

    central_frame = tk.Frame(root, bg="grey24")
    central_frame.pack(side="top", expand=True)

    module_label = tk.Label(central_frame, text=f"Module: {module_name}", font=("Helvetica", 18), fg="white", bg="grey24")
    module_label.pack(pady=20)

    launch_button = tk.Button(central_frame, text="Launch", bg="green", fg="white", command=lambda: launch_module(module_name))
    launch_button.pack(pady=20)


def launch_module(module_name: str) -> None:
    for module_path, module_info in loaded_modules.items():
        if os.path.basename(module_path) == module_name:
            print(f"Launching {module_name}")

            for func_name, func_doc in module_info["functions"].items():
                default_modules[func_name]() 
            break


def create_module_buttons(root, left_frame) -> None:

    for widget in left_frame.winfo_children():
        widget.destroy()

    for module_path, module_info in loaded_modules.items():
        module_name = os.path.basename(module_path)
        button = tk.Button(left_frame, text=module_name, width=20, bg="grey24", fg="white", command=lambda m=module_name: show_module_info(root, left_frame, m))
        button.pack(side="top", padx=5, pady=5)


def the_carcass_gui(the_global_version: str) -> None:
    global root
    root = tk.Tk()
    root.title("theSuffocater GUI")
    root.geometry("700x500")
    root.config(bg="grey24")

    
    def import_m() -> None:
        import_modules(root, left_frame)

    
    def exit() -> None:
        final_exit(root)

    
    def list() -> None:
        list_imported_modules(root)

    
    def version() -> None:
        the_global_version(root)

    
    def documentation() -> None:
        the_suffocater_documentation(root)

    
    def license() -> None:
        the_suffocater_license(root)

    
    def changelod() -> None:
        the_suffocater_changelog(root)

    top_frame = tk.Frame(root, bg="grey29")
    top_frame.pack(side="top", fill="x")
    
    left_frame = tk.Frame(root, width=190, bg="grey20")
    left_frame.pack(side="left", fill="y")

    right_frame = tk.Frame(root, width=130, bg="grey20")
    right_frame.pack(side="right", fill="y")

    tk.Button(top_frame, text="Import modules", width=20, command=import_m,  bg="grey24", fg="white").pack(side="left", fill="x", padx=5, pady=5)
    tk.Button(top_frame, text="Exit", width=3, bg="grey20", fg="white", activeforeground="red", command=exit).pack(side="right", padx=5, pady=5)
    tk.Button(right_frame, text="list", width=20, command=list).pack(side="top",padx=5, pady=5)
    tk.Button(right_frame, text="Version", width=20, command=version).pack(side="top",padx=5, pady=5)
    tk.Button(right_frame, text="Documentation", width=20, command=documentation).pack(side="top",padx=5, pady=5)
    tk.Button(right_frame, text="License", width=20, command=license).pack(side="top",padx=5, pady=5)
    tk.Button(right_frame, text="Changelog", width=20, command=changelod).pack(side="top",padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    default_modules: dict = {
            "exit": final_exit,
            "import": import_modules,
            "modules": list_imported_modules,
            "modules -d": lambda: list_imported_modules(show_docs=True),
            "license": the_suffocater_license,
            "changelog": the_suffocater_changelog,
            "documentation": the_suffocater_documentation,
            "global_version": the_suffocater_version_string and the_carcass_version_string
    }
    tum.clear_screen()
    the_carcass_gui(the_global_version)
