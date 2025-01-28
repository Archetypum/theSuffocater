#!/usr/bin/python3

"""
---------------------------------------
For backing up files and databases.

Author: zaw.
Date: 19.01.2025
---------------------------------------
"""

try:
    import os
    import shutil
    import sqlite3
    from sys import exit
    from datetime import datetime
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found.\n{import_error}.{RESET}")
    exit(1)


def backup_files() -> None:
    """
    
    """

    source_directory: str = input('[==>] Enter the source directory: ')
    backup_directory: str = input('[==>] Enter the backup directory: ')

    if not os.path.exists(source_directory):
        print(f"{RED}[!] Error: Could not find source directory: {source_directory}{RESET}")
        return

    if not os.path.exists(backup_directory):
        print(f"{RED}[!] Error: Unable to find backup directory.{RESET}")

        if tum.prompt_user("[?] Create a new directory?"):
            os.makedirs(backup_directory)
            print(f"{GREEN}[*] Directory created successfully.{RESET}")
        else:
            print("[*] Exiting without creating backup directory.")
            return

    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_backup_directory: str = os.path.join(backup_directory, f"backup_files_{timestamp}")
    os.makedirs(timestamped_backup_directory)
                
    for item in os.listdir(source_directory):
        source_item: str = os.path.join(source_directory, item)
        backup_item: str = os.path.join(timestamped_backup_directory, item)

        if not os.path.exists(source_item):
            print(f"{RED}[!] Error: Could not find the file: {source_item}{RESET}")
            return

        if os.path.isdir(source_item):
            shutil.copytree(source_item, backup_item)
            print(f"{GREEN}[*] Directory backup completed: {backup_item}{RESET}")
        else:
            shutil.copy2(source_item, backup_item)
            print(f"{GREEN}[*] File backup completed: {backup_item}{RESET}")

            
def backup_database() -> None:
    """
    
    """
   
    database_path: str = input("[==>] Enter the path to the source database file: ")
    database_backup_directory: str = input("[==>] Enter the path to the directory for the database backup: ")
  
    if not os.path.exists(database_path):
        print(f"{RED}[!] Unable to find database: {database_path}{RESET}")
        return

    if not os.path.exists(database_backup_directory):
        print("[!] Unable to find backup directory")

        if tum.prompt_user("[?] Create a new directory?"):
            os.makedirs(database_backup_directory)
            print(f"{GREEN}[*] Directory created successfully.{RESET}")
        else:
            print("[*] Exiting without creating backup directory.")
            return
    
    if not os.path.exists(database_path):
        print(f"{RED}[!] Unable to find database file: {database_path}{RESET}")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_backup_directory: str = os.path.join(database_backup_directory, f"backup_db_{timestamp}")
    os.makedirs(timestamped_backup_directory)

    database_name: str = os.path.basename(database_path)
    backup_database_name: str = f"{database_name}_{timestamp}.bak"
    backup_database_path: str = os.path.join(timestamped_backup_directory, backup_database_name)

    shutil.copy2(database_path, backup_database_path)
    print(f"{GREEN}[*] Database backup completed: {backup_database_path}{RESET}")


def backup_management() -> None:
    """
    [*] MAIN FUNCTION [*]
    """
    
    tum.clear_screen()
       
    functions: dict = {
        "backup_files": backup_files,
        "backup_database": backup_database
    }

    print("+---- Backup Management ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    try:
        while True:
            your_function: str = input("[==>] Enter function: ").lower()
            if your_function in functions:
                functions[your_function]()
            else:
                print(f"{RED}[!] Error: '{your_function}' not found.{RESET}")
    except KeyboardInterrupt:
        print("\n")
        pass


if __name__ == "__main__":
    backup_management()
