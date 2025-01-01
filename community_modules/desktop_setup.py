#!/usr/bin/python3

"""
---------------------------------------
Installs and configures:
 - X11.
 - Wayland.
 - Any graphical enviroment.
 - Free/proprietary NVIDIA drivers.

Author: iva
Date: null
---------------------------------------
"""

try:
    import os
    import usr
    import subprocess
    from sys import exit
    from os import system
    from time import sleep
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def desktop_setup() -> None:
    print("null")


if __name__ == "__main__":
    desktop_setup()
