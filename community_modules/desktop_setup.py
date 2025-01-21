#!/usr/bin/python3

"""
---------------------------------------
Installs and configures:
 - X11.
 - Wayland.
 - Any graphical environment.
 - Free/proprietary NVIDIA drivers.
GNU/Linux supported.

Author: iva
Date: null
---------------------------------------
"""

try:
    import os
    import subprocess
    from sys import exit
    from os import system
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: Modules not found:\n{import_error}{RESET}")


def desktop_setup() -> None:
    """
    Main function.
    """

    tum.clear_screen()

    print("null")


if __name__ == "__main__":
    desktop_setup()
