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
    ...


if __name__ == "__main__":
    fail2ban_setup()
