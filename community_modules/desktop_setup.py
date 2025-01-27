#!/usr/bin/python3

"""
---------------------------------------
Installs and configures:
 - X11.
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


def install_nvidia_free() -> None:
    """
    Installs NVIDIA nouveau drivers.

    Returns:
        None: None.
    """

    distro: str = tum.get_user_distro()

    try:
        print("We are going to install free nouveau NVIDIA drivers.")
        if tum.prompt_user("[?] Proceed?"):
            tum.package_handling(distro, ["xserver-xorg-video-nouveau", "mesa-utils", "mesa", "libgl1-mesa-dri", "libgl1-mesa-glx"], "install")

            if tum.prompt_user("[?] Install Vulkan?"):
                tum.package_handling(distro, ["libvulkan1", "vulkan-utils"], "install")

            if tum.prompt_user("[?] Update initramfs?"):
                subprocess.run(["update-initramfs", "-u"], check=True)

            print(f"{GREEN}[*] Success!{RESET}")
    except subprocess.CalledProcessError as x11_installation_error:
        print(f"{RED}[!] Error: {x11_installation_error}{RESET}")
        pass

    except KeyboardInterrupt:
        print("\n")
        pass


def install_nvidia_proprietary() -> None:
    """
    Installs proprietary NVIDIA drivers.

    Returns:
        None: None.
    """

    distro: str = tum.get_user_distro()
    nvidia_drivers: list = ["nvidia-detect", "nvidia-driver", ""]
    try:
        print("We are going to install proprietary NVIDIA drivers:")
        if tum.prompt_user("[?] Proceed?"):
            ...

    except KeyboardInterrupt:
        print("\n")
        pass


def install_x11() -> None:
    """
    Installs X11-server.

    Returns:
        None: None.
    """
    
    distro: str = tum.get_user_distro()

    try:
        print("We are going to install X Window System.")
        if tum.prompt_user("[?] Proceed?"):
            tum.package_handling(distro, ["xorg", "xinit", "xterm"], "install")

            if tum.prompt_user("[?] Install ttf-fonts?"):
                tum.package_handling(distro, ["ttf-mscorefonts-installer"], "install")

            if tum.prompt_user("[?] Add user to video group?"):
                user_to_add: str = input("[==>] Enter user: ")
                try:
                    subprocess.run(["usermod", "-aG", "video", user_to_add], check=True)
                except subprocess.CalledProcessError as usermod_error:
                    print(f"{RED}[!] Error: {usremod_error}")

            print(f"{GREEN}[*] Success!{RESET}")
    except KeyboardInterrupt:
        print("\n")
        pass


def install_dm_wm_de() -> None:
    """
    Installs popular Display Managers, Window Managers, and Desktop Enviroments.

    Returns:
        None: None.
    """
    
    distro: str = tum.get_user_distro()
    display_managers: list = ["LightDM", "GMD3", "SDDM", "XDM", "WDM", "LXDM", "CDM"]
    window_managers: list = ["Awesome", "i3", "Openbox", "Fluxbox", "Xmonad", "dwm", "swm"]
    desktop_enviroments: list = ["GNOME", "KDE Plasma", "XFCE", "LXDE", "LXQt", "MATE", "Cinnamon", "Budgie", "Lumina", "Equinox"]
    
    try:
        print("\nDisplay Managers:")
        for dm in display_managers:
            print(f" - {dm}")

        print("\nDesktop Enviroments:")
        for de in desktop_enviroments:
            print(f" - {de}")

        print("\nWindow Managers:")
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
    [*] MAIN FUNCTION [*]
    """

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
