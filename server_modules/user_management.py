#!/usr/bin/python3

"""
---------------------------------------
UNIX user management for noobs.
GNU/Linux and BSD supported.

Author: iva
Date: 05.12.2024
---------------------------------------
"""

try:
    import pwd
    import grp
    import subprocess
    from sys import exit
    from getpass import getpass
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")
    exit(1)


def add_user(username: str = None, password: str = None, group: str = None) -> None:
    """
    Adds user to the system.

    Args:
        username (str): Name of the new user. None by default.
        password (password): Password for the new user. None by default.
        group (str): Group for new user. None by default.

    Returns:
        None: None.
    """

    if username is None:
        username: str = input("\n[==>] Enter username: ")

    if password is None:
        password: str = input("\n[==>] Enter password: ")

    if group is None:
        group: str = input("\n[==>] Enter group: ")

    try:
        if group:
            subprocess.run(["useradd", "-m", "-g", group, username], check=True)
        else:
            subprocess.run(["useradd", "-m", username], check=True)
        
        passwd_process: subprocess.Popen[bytes] = subprocess.Popen(
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


def remove_user(username: str = None) -> None:
    """
    Removes user from the system.

    Args:
        username (str): User to remove. None by default.
    """
    
    if username is None:
        username: str = input("\n[==>] Enter username: ")

    try:
        subprocess.run(["userdel", "-r", username], check=True)
        print(f"{GREEN}[*] User '{username}' removed successfully.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error removing user '{username}': {error}{RESET}")


def change_group(username: str = None, group: str = None) -> None:
    """
    Changes user groups.

    Args:
        username (str): Target user to add to group. None by default.
        group (str): Target group. None by default.

    Returns:
        None: None.
    """

    if username is None:
        username: str = input("\n[==>] Enter username: ")

    if group is None:
        group: str = input("\n[==>] Enter group: ")

    try:
        subprocess.run(["usermod", "-g", group, username], check=True)
        print(f"{GREEN}[*] User '{username}' is now in the group '{group}'.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error changing group for '{username}': {error}{RESET}")


def list_users() -> None:
    """
    Lists users in the system.

    Returns:
        None: None.
    """

    users: list = [user.pw_name for user in pwd.getpwall()]
    print("Users in the system:")
    for user in users:
        print(f" - {user}")


def list_groups() -> None:
    """
    Lists groups in the system.
    
    Returns:
        None: None.
    """

    groups: list = [g.gr_name for g in grp.getgrall()]
    print("Groups in the system:")
    for group in groups:
        print(f" - {group}")


def view_groups(username: str = None) -> None:
    """
    Returns list of groups that user belongs to.

    Returns:
        None: None.
    """
    
    if username is None:
        username: str = input("\n[==>] Enter user: ")

    try:
        user_info: pwd.struct_passwd = pwd.getpwnam(username)
        groups: list = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]
        
        if groups:
            print(f"User {username} belongs to the following groups:")
            for group in groups:
                print(group)
        else:
            print(f"{RED}[!] User '{username}' does not belong to any groups.{RESET}")
    except KeyError:
        print(f"{RED}[!] User '{username}' not found.{RESET}")


def add_user_to_group(username: str = None, group: str = None) -> None:
    """
    Adds user to group via usermod.

    Args:
        username (str): User to add. None by default.
        group (str): Group to add user. None by default.

    Returns:
        None: None.
    """

    if username is None:
        username: str = input("\n[==>] Enter user: ")

    if group is None:
        group: str = input("[==>] Enter group: ")

    try:
        subprocess.run(["usermod", "-aG", group, username], check=True)
        print(f"{GREEN}[*] User '{username}' added to group '{group}'.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error adding '{username}' to group '{group}': {error}{RESET}")


def remove_user_from_group(username: str = None, group: str = None) -> None:
    """
    Removes user from group via gpasswd.

    Args:
        username (str): User to remove from group. None by default.
        group (str): Group to remove user from. None by default.

    Returns:
        None: None.
    """
    
    if username is None:
        username: str = input("\n[==>] Enter user: ")

    if group is None:
        group: str = input("[==>] Enter group: ")

    try:
        subprocess.run(["gpasswd", "-d", username, group], check=True)
        print(f"{GREEN}[*] User '{username}' removed from group '{group}'.{RESET}")
        user_management()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error removing '{username}' from group '{group}': {error}{RESET}")


def user_management() -> None:
    """
    [*] MAIN FUNCTION [*]
    """

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
    
    try:
        while True:
            if your_function in functions:
                if your_function == "add_user":
                    username: str = input("[==>] Enter username: ")
                    password: str = getpass("[==>] Enter password (will not echo): ")
                    group: str = input("[==>] Enter group (optional): ") or None
                    functions[your_function](username, password, group)
                elif your_function == "remove_user" or your_function == "change_group" or your_function == "view_groups":
                    username: str = input("[==>] Enter username: ")
                    functions[your_function](username)
         
                if your_function == "change_group":
                    group: str = input("[==>] Enter group: ")
                    functions[your_function](username, group)
                else:
                    functions[your_function](username)
            elif your_function in ["list_users", "list_groups"]:
                functions[your_function]()
    except KeyboardInterrupt:
        print("\n")
        pass


if __name__ == "__main__":
    user_management()
