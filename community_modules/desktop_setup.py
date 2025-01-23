#!/usr/bin/python3

"""
---------------------------------------
Installs and configures:
 - X11.
 - Any graphical environment.
 - Free/proprietary NVIDIA drivers.
GNU/Linux supported, BSD supported.

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

    try:
        print("We are going to install X Window System.")
        if tum.prompt_user("[?] Proceed?"):
            tum.package_handling(distro, ["xorg", "xinit", "xterm"], "install")
    except KeyboardInterrupt:
        print("\n")
        pass


def install_dm_wm_de() -> bool:
    """
    Installs popular Display Managers, Window Managers, and Desktop Enviroments.

    Returns:
        bool: Installation status.
    """
    
    distro: str = tum.get_user_distro()

    display_managers: list = ["LightDM", "GMD3", "SDDM", "XDM", "WDM", "LXDM", "CDM"]
    window_managers: list = ["Awesome", "i3", "Openbox", "Fluxbox", "Xmonad", "dwm", "swm"]
    desktop_enviroments: list = ["GNOME", "KDE Plasma", "XFCE", "LXDE", "LXQt", "MATE", "Cinnamon", "Budgie", "Lumina", "Equinox"]
    
    try:
        print("Display Managers:")
        for dm in display_managers:
            print(f" - {dm}")

        print("Desktop Enviroments:")
        for de in desktop_enviroments:
            print(f" - {de}")

        print("Window Managers:")
        for wm in window_managers:
            print(f" - {wm}")
        
        graphics_to_install: str = input("[==>] Enter package to install: ")
        if graphics_to_install in [display_managers, window_managers, desktop_enviroments]:
            tum.package_handling(distro, [graphics_to_install], "install")
    except KeyboardInterrupt:
        print("\n")
        pass
    

def desktop_setup() -> None:
    """
    Main function.
    """

    tum.clear_screen()

    functions: dict = {
            "install_x11": install_x11,
            "configure_x11": configure_x11,
            "install_dm_wm_de": install_dm_wm_de,
            "install_nvidia_free": install_nvidia_free,
            "install_nvidia_proprietary": install_nvidia_proprietary
    }

    print("+---- Desktop Setup ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__":
    desktop_setup()
