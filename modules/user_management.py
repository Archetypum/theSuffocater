#!/usr/bin/python3

"""
---------------------------------------
Unix user management for noobs.
GNU/Linux and BSD supported.

Author: iva
Date: 05.12.2024
---------------------------------------
"""

try:
    import usr
    import pwd
    import grp
    import subprocess
    from sys import exit
    from getpass import getpass
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"[!] Error: modules not found:\n{error}")
    exit(1)


def add_user(username: str, password: str, group: str = None) -> None:
    try:
        if group:
            subprocess.run(["useradd", "-m", "-g", group, username], check=True)
        else:
            subprocess.run(["useradd", "-m", username], check=True)
        
        passwd_process: str = subprocess.Popen(
            ["passwd", username],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        passwd_process.communicate(input=f"{password}\n{password}\n".encode())

        if passwd_process.returncode == 0:
            print(f"{GREEN}[*] User '{username}' added and password set successfully.{RESET}")
        else:
            print(f"{RED}[!] Error setting password for user '{username}'.{RESET}")
            return
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error adding user '{username}': {error}{RESET}")


def remove_user(username: str) -> None:
    try:
        subprocess.run(["userdel", "-r", username], check=True)
        print(f"{GREEN}[*] User '{username}' removed successfully.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error removing user '{username}': {error}{RESET}")


def change_group(username: str, group: str) -> None:
    try:
        subprocess.run(["usermod", "-g", group, username], check=True)
        print(f"{GREEN}[*] User '{username}' is now in the group '{group}'.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error changing group for '{username}': {error}{RESET}")


def list_users() -> None:
    try:
        users: list = [user.pw_name for user in pwd.getpwall()]
        print("Users in the system:")
        for user in users:
            print(f" {user}")
        user_management()
    except Exception as error:
        print(f"{RED}[!] Error: {error}{RESET}")


def list_groups() -> None:
    try:
        groups: list = [g.gr_name for g in grp.getgrall()]
        print("Groups in the system:")
        for group in groups:
            print(f" {group}")
        user_management()
    except Exception as error:
        print(f"{RED}[!] Error: {error}{RESET}")


def view_groups(username: str) -> None:
    try:
        user_info: str = pwd.getpwnam(username)
        groups: list = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
        
        if groups:
            print(f"User {username} belongs to the following groups:")
            for group in groups:
                print(group)
        else:
            print(f"{RED}[!] User '{username}' does not belong to any groups.{RESET}")

        user_management()
    except KeyError:
        print(f"{RED}[!] User '{username}' not found.{RESET}")


def add_user_to_group(username: str, group: str) -> None:
    try:
        subprocess.run(["usermod", "-aG", group, username], check=True)
        print(f"{GREEN}[*] User '{username}' added to group '{group}'.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error adding '{username}' to group '{group}': {error}{RESET}")

def remove_user_from_group(username: str, group: str) -> None:
    try:
        subprocess.run(["gpasswd", "-d", username, group], check=True)
        print(f"{GREEN}[*] User '{username}' removed from group '{group}'.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error removing '{username}' from group '{group}': {error}{RESET}")


def user_management() -> None:
    functions: dict = {
        "add_user": add_user,
        "remove_user": remove_user,
        "change_group": change_group,
        "list_users": list_users,
        "list_groups": list_groups,
        "view_groups": view_groups,
        "add_user_to_group": add_user_to_group,
        "remove_user_from_group": remove_user_from_group
    }
    
    print("+---- User Management  ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name: ").lower()

    if your_function in functions:
        if your_function == "add_user":
            username: str = input("[==>] Enter username: ")
            password: str = getpass("[==>] Enter password (will not echo): ")
            group: str = input("[==>] Enter group (optional): ") or None
            functions[your_function](username, password, group)
        elif your_function == "remove_user" or your_function == "change_group" or your_function == "view_groups":
            username: str = input("[==>] Enter username: ")
            if your_function == "change_group":
                group: str = input("[==>] Enter group: ")
                functions[your_function](username, group)
            else:
                functions[your_function](username)
        elif your_function in ["list_users", "list_groups"]:
            functions[your_function]()


if __name__ == "__main__":
    user_management()

