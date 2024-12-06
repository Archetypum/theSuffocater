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
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")


def system_monitor() -> None:
    ...
