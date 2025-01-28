#!/usr/bin/python3

"""
---------------------------------------
Setup your VPN servers automatically with this module.
GNU/Linux and BSD supported (OpenVPN, Wireguard)
GNU/Linux supported (OutlineVPN)

Author: iva
Date: 18.10.2024
---------------------------------------
"""

try:
    import subprocess
    from sys import exit
    from time import sleep
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")
    exit(1)


def openvpn_server_setup() -> None:
    """
    Setups OpenVPN server using preinstalled bash script.

    Returns:
        None: None.
    """

    distro: str = tum.get_user_distro()
    init_system: str = tum.get_init_system()
    print("\nWe are going to setup OpenVPN server.")
    if tum.prompt_user("\n[?] Proceed?"):
        try:
            print("[<==] Updating the system...")
            tum.package_handling(distro, package_list=[], command="update")
            
            print("[<==] Installing OpenVPN...")
            tum.package_handling(distro, package_list=["openvpn"], command="install")
            
            print("[<==] Launching OpenVPN-Installer script...")
            subprocess.run(["bash", "/root/.scripts/openvpn-install.sh"], check=True)
            sleep(1)

            print("[<==] Restarting OpenVPN service && Finishing installation...")
            tum.init_system_handling(init_system, "start", "openvpn")
            
            print("[*] Looks like you are locked and loaded.\nNow, move your *.ovpn configuration file to your client and enjoy the freedom.")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def wireguard_server_setup() -> None:
    """
    Setups Wireguard server using preinstalled bash script.

    Returns:
        None: None.
    """

    distro: str = tum.get_user_distro()
    init_system: str = tum.get_init_system()

    print("\nWe are going to setup your server for Wireguard.")
    if tum.prompt_user("\n[?] Proceed?"):
        try:
            print("[<==] Updating the system...")
            tum.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing Wireguard...")
            tum.package_handling(distro, package_list=["wireguard", "wireguard-tools"], command="install")

            print("[<==] Launching Wireguard-Installer script...")
            subprocess.run(["bash", "/root/.scripts/wireguard-install.sh"], check=True)
            sleep(1)

            print("[<==] Restarting Wireguard service && Finishing installation...")
            tum.init_system_handling(init_system, "start", "wireguard")

            print("[*] Looks like you are locked and loaded.\nEnjoy your freedom.")
        except subprocess.CalledProcessError as error:
            print(f"{RED} Error: {error}{RESET}")


def outlinevpn_server_setup() -> None:
    """
    Setups OutlineVPN server for you.

    Returns:
        None: None.
    """

    distro: str = tum.get_user_distro()
    init_system: str = tum.get_init_system()

    print("We are going to setup your server for OutlineVPN.") 
    answer: str = input("\n[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            print("[<==] Updating the system...")
            tum.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing Docker...")
            subprocess.run(["wget", "https://get.docker.com", "-O", "get-docker.sh"], check=True)
            subprocess.run(["bash", "get-docker.sh"], check=True)
            
            print("[<==] Starting Docker...")
            tum.init_system_handling(init_system, "start", "docker")

            print("[*] Looks like you are locked and loaded.\nNow, check the instructions in Outline Manager.")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def vpn_server_setup() -> None:
    """
    [*] MAIN FUNCTION [*]
    """

    functions: dict = {
            "openvpn_server_setup": openvpn_server_setup,
            "wireguard_server_setup": wireguard_server_setup,
            "outlinevpn_server_setup": outlinevpn_server_setup
            }

    print("+---- VPN Server Setup ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    try:
        while True:
            your_function: str = input("[==>] Enter function: ").lower()
            if your_function in functions:
                functions[your_function]()
            else:
                print(f"{RED}[!] Error: '{your_function}' not found.{RESET}")
    except KeyboardInterrupt:
        print("\n")
        pass


if __name__ == "__main__":
    vpn_server_setup()
