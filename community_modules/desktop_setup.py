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


def install_nvidia_free() -> bool:
    """
    Installs NVIDIA nouveau drivers.

    Returns:
        bool: Installation status.
    """

    ...


def install_nvidia_proprietary() -> bool:
    """
    Installs proprietary NVIDIA drivers.

    Returns:
        bool: Installation status.
    """

    ...


def configure_x11() -> bool:
    """
    Configures X11-server.

    Returns:
        bool: Configuration status.
    """

    ...


def install_x11() -> bool:
    """
    Installs X11-server.

    Returns:
        bool: Installation status.
    """
    
    distro: str = tum.get_user_distro()

    print("We are going to install X Window System.")
    if tum.prompt_user("[?] Proceed"):
        tum.package_handling(distro, ["xorg", "xinit", "xterm"], "install")


def configure_wayland() -> bool:
    """
    Configures Wayland.
    
    Returns:
        bool: Installlation status.
    """

    distro: str = tum.get_user_distro()

    print("We are going to install Wayland FreeDesktop.")
    if tum.prompt_user("[?] Proceed"):
        tum.package_handling(distro, [""], "install")


def install_wayland() -> bool:
    """
    Installs Wayland.

    Returns:
        bool: Installation status.
    """

    ...


def install_dm_wm_de() -> bool:
    """
    Installs popular Display Managers, Window Managers, and Desktop Enviroments.

    Returns:
        bool: Installation status.
    """

    display_managers: list = []
    window_managers: list = []
    desktop_enviroments: list = ["GNOME", "KDE Plasma", "XFCE", "LXDE", "LXQt", "MATE", "Cinnamon", "Budgie", "Lumina"]


def desktop_setup() -> None:
    """
    Main function.
    """

    print("null")


if __name__ == "__main__":
    desktop_setup()
