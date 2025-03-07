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
    """
    Exits theSuffocater.

    Returns:
        None: [null].
    """

    root.quit()


def import_modules() -> None:
    """
    Gets path, then imports modules.
    
    Returns:
        None: [null].
    """

    directory_path: str = simpledialog.askstring("Enter modules directory path (e.g /home/$USER/Desktop/my_python_modules)", "[==>] ", parent=root)
    if not os.path.isdir(directory_path):
        messagebox.showerror("[!] Error", "Not a directory.", parent=root)
        return

    import_functions_from_directory(directory_path)
    module_buttons()


def list_imported_modules(show_docs: bool = False) -> None:
    """
    Lists imported modules and docstrings.

    Args:
        show_docs (bool): If enabled, prints function docstrings too.

    Returns:
        None: [null].
    """

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


def import_functions_from_directory(directory_path: str) -> None:
    """
    Imports python file functions and docstrings from specified directory
    for further usage in theSuffocater.

    Args:
        directory_path (str): Path to directory with .py files.

    Returns:
        None: [null].
    """
    
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
                messagebox.showerror("[!] Error", "Can't import module.", parent=root)


def import_modules_from_config() -> None:
    """
    Import python modules from config file located in '/etc/tsf/module_configs/import_py.conf'
    using their paths (if exists).
    
    Config file is empty by default.

    Returns:
        None: [null].
    """

    config_file_path: str = "/etc/tsf/module_configs/import_py.conf"
    if not os.path.exists(config_file_path):
        print(f"[!] Error: Configuration file 'import_py.conf' not found!")
        return
    
    try:
        with open(config_file_path, "r") as config_file:
            module_paths: list = config_file.readlines()
        
        module_paths: list = [path.strip() for path in module_paths if path.strip()] 
        if not module_paths:
            print(f"{RED}[!] Error: No module paths found in 'import_py.conf'.{RESET}")
            return

        for directory_path in module_paths:
            if not os.path.isdir(directory_path):
               print(f"{RED}[!] Error: '{directory_path}' is not a valid directory.{RESET}")

            import_functions_from_directory(directory_path)
    except IOError as processing_error:
        print(f"{RED}[!] Error: Error while reading or processing the config file: {processing_error}{RESET}")


def show_module_info(module_name: str) -> None:
    """
    Displays modules and information about them in the GUI.

    Args:
        module_name (str).
    
    Returns:
        None: [null].
    """

    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget != left_frame and widget != top_frame:
            widget.destroy()

    central_frame = tk.Frame(root, bg="grey24")
    central_frame.pack(side="left", fill="both", expand=True)

    module_label = tk.Label(central_frame, text=f"Module: {module_name}", font=("Helvetica", 18), fg="white", bg="grey24")
    module_label.pack(pady=20, expand=True)

    for module_path, module_info in loaded_modules.items():
        if os.path.basename(module_path) == module_name:
            module_docstring = module_info['docstring']
            docstring_label = tk.Label(central_frame, text=f"Docstring: {module_docstring or 'None'}", font=("Helvetica", 12), fg="lightgrey", bg="grey24")
            docstring_label.pack(pady=10, expand=True)

    launch_button = tk.Button(central_frame, text="Launch", width=50, bg="green", fg="white", command=lambda: launch_module(module_name))
    launch_button.pack(pady=20, expand=True)


def launch_module(module_name: str) -> None:
    """
    Launches modules and their main functions.

    Args:
        module_name (str)
    
    Returns:
        None: [null].
    """

    for module_path, module_info in loaded_modules.items():
        if os.path.basename(module_path) == module_name:
            print(f"Launching {module_name}")

            main_func_name = os.path.splitext(module_name)[0]
            if main_func_name in module_info["functions"]:
                default_modules[main_func_name]()
            else:
                messagebox.showerror("[!]", "Main function not found.")


def module_buttons() -> None:
    """
    Creates module buttons, slider and many other graphic elements.

    Returns:
        None: [null].
    """

    for widget in left_frame.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(left_frame, bg="grey20", width=200)
    canvas.pack(side="left", fill="y")

    scrollbar = tk.Scrollbar(left_frame, bg="grey20", orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.config(yscrollcommand=scrollbar.set)

    button_frame = tk.Frame(canvas, bg="grey24")
    canvas.create_window((0, 0), window=button_frame, anchor="nw")

    for module_path, module_info in loaded_modules.items():
        module_name = os.path.basename(module_path)
        
        button = tk.Button(button_frame, text=module_name, width=20, bg="grey24", fg="white",
            command=lambda m=module_name: show_module_info(m))
        button.pack(side="top", padx=5, pady=5)

    button_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def get_markdown(preferred_text_editor, document: str) -> None:
    """
    Gets Markdown documents from '/etc/tsf/markdown' and prints them with 'less' command.

    Args:
        document (str): Document specified by user. 'LICENSE.md', 'DOCUMENTATION.md', 'CHANGELOG.md' are available.
        None by default

    Returns:
        None: [null].
    """

    editor = simpledialog.askstring("[==>]", "Enter the preferred text editor:")
    preferred_text_editor = editor if editor else "less"

    try:
        if document is None:
            print(f"{RED}[!] Error: Document not specified.{RESET}")
        else:
            run([f"{preferred_text_editor}", f"/etc/tsf/markdown/{document}"], check=True)
    except (FileNotFoundError, CalledProcessError):
        messagebox.showerror("[!] Error", "File not found. Broken installation?")


def get_version(component: str = None) -> None:
    """
    Gets version files from '/etc/tsf/versions' (at the top of theCarcass) and prints them.

    Args:
        component (str).
    
    Returns:
        None: [null].
    """

    messagebox.showinfo("Version", f"Current theSuffocater version - {the_suffocater_version_string} \nCurrent theCarcass version - {the_carcass_version_string}")


if __name__ == "__main__":
    """
    [*] MAIN FUNCTION [*]
    """
    default_modules: dict = {
            "exit": final_exit,
            "import": import_modules,
            "modules": list_imported_modules,
            "modules -d": lambda: list_imported_modules(show_docs=True),
            "license": lambda: get_markdown(document="LICENSE-GPL.md"),
            "changelog": lambda: get_markdown(document="CHANGELOG.md"),
            "documentation": lambda: get_markdown(document="README.md"),
            "get_version": the_suffocater_version_string and the_carcass_version_string
    }
    
    import_modules_from_config()

    root = tk.Tk()
    root.title("theSuffocater")
    root.geometry("850x600")
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

    import_modules_button = tk.Button(top_frame, text="Import modules", width=20, activeforeground="blue", command=import_modules,  bg="grey24", fg="white")
    import_modules_button.pack(side="left", fill="x", padx=5, pady=5)

    exit_button = tk.Button(top_frame, text="Exit", width=3, bg="grey20", fg="white", activeforeground="red", command=final_exit)
    exit_button.pack(side="right", padx=5, pady=5)
    
    list_button = tk.Button(top_frame, text="list", width=10, command=list_imported_modules)
    list_button.pack(side="left", padx=5, pady=10)

    versions_button = tk.Button(top_frame, text="Version", width=10, command=get_version)
    versions_button.pack(side="left", padx=5, pady=10)

    documentation_button = tk.Button(top_frame, text="Documentation", width=10, command=lambda: get_markdown(preferred_text_editor="less", document="README.md"))
    documentation_button.pack(side="left", padx=5, pady=10)

    license_button = tk.Button(top_frame, text="License", width=10, command=lambda: get_markdown(preferred_text_editor="less", document="LICENSE-GPL.md"))
    license_button.pack(side="left", padx=5, pady=5)

    changelog_button = tk.Button(top_frame, text="Changelog", width=10, command=lambda: get_markdown(preferred_text_editor="less", document="CHANGELOG.md"))
    changelog_button.pack(side="left", padx=5, pady=5)
    
    root.mainloop()
