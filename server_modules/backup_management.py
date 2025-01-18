#!/usr/bin/python3

"""
---------------------------------------
Backs up files and databases.
Author: zaw.
Date: 19.01.25
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
    tum.clear_screen()

    # Path to directory for file backup
    source_directory: str = input('[==>] Enter the source directory: ')
    backup_directory: str = input('[==>] Enter the backup directory: ')

    if not os.path.exists(backup_directory):
        print("[!] Unable to find backup directory")
        dir_create_answer: str = input("[?] Create a new directory(y/n)?: ")        
        
        if dir_create_answer.lower() in ['y', 'yes']:
            os.makedirs(backup_directory)
        
            if not os.path.exists(backup_directory):
                print(f"{RED}[!] Error: Failed to create directory: {error}{RESET}")
                return
            else:
                print(f"{GREEN}[*] Directory created successfully.{RESET}")
        else:
            print("[!] Exiting without creating backup directory.")
            return
                    
    for item in os.listdir(source_directory):
        source_item = os.path.join(source_directory, item)
        backup_item = os.path.join(backup_directory, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, backup_item)
            print(f"{GREEN}[*]File backup completed: {backup_directory}{RESET}")
        else:
            shutil.copy2(source_item, backup_item)
            print(f"{GREEN}[*] File backup completed: {backup_item}{RESET}")

def backup_database() -> None:
    tum.clear_screen()
   
    # Path to SQLite database
    database_path: str = input('[==>]Enter the path to the source database file: ')
    database_backup_directory: str = input('[==>]Enter the path to the directory for the database backup: ')
  
    if not os.path.exists(database_backup_directory):
        os.makedirs(database_backup_directory)

        if not os.path.exists(database_backup_directory):
            print(f"{RED}[!] Error: Failed to create directory: {error}{RESET}")
            return

    database_name = os.path.basename(database_path)
    backup_database_name = f"{database_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    backup_database_path = os.path.join(database_backup_directory, backup_database_name)

    shutil.copy2(database_path, backup_database_path)
    print(f"{GREEN}[*]Database backup completed: {backup_database_path}{RESET}")


def backup_management() -> None:
    tum.clear_screen()
       
    functions: dict = {
        "backup_files": backup_files,
        "backup_database": backup_database
    }

    print("+---- Backup Management ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function: ").lower()
    if your_function in functions:
        functions[your_function]()
    else:
        print(f"{RED}[!] No such function.{RESET}")


if __name__ == "__main__":
    backup_management()

