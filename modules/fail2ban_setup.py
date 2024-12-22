#!/usr/bin/python3

"""
---------------------------------------
null

GNU/Linux, BSD supported.
Author: iva
Date: null
---------------------------------------
"""

try:
    import usr
    import subprocess
    from sys import exit
    from os import system
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def fail2ban_setup() -> None:
    system("clear")

    profiles: dict = {}
    
    print("+---- Fail2Ban Setup ----+")
    print("\nAvailable functions:")
    for profile in profiles.keys():
        print(f" - {function}")
    
    while True:
        try:
            your_profile: str = input("[==>] Enter profile: ").lower()
            if your_profile in profiles:
                profiles[your_profile]()
            else:
                print(f"{RED}[!] Error: {your_profile} is not defined.{RESET}")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    fail2ban_setup()
