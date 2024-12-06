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
    import usr
    import subprocess
    from sys import exit
    from os import system
    from time import sleep
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")
    exit(1)


def openvpn_server_setup() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()

    print("We are going to setup your server for OpenVPN.")
    answer: str = input("\n[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            print("[<==] Updating the system...")
            usr.package_handling(distro, package_list=[], command="update")
            
            print("[<==] Installing OpenVPN...")
            usr.package_handling(distro, package_list=["openvpn"], command="install")
            
            print("[<==] Installing Curl...")
            usr.package_handling(distro, package_list=["curl"], command="install")

            print("[<==] Installing OpenVPN-Installer script...")
            subprocess.run(["curl", "-LJO", "https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh"], check=True, shell=True)
            subprocess.run(["chmod", "+x", "openvpn-install.sh"], check=True, shell=True)
            subprocess.run(["bash", "./openvpn-install.sh"], check=True, shell=True)
            sleep(1)

            print("[<==] Restarting OpenVPN service && Finishing installation...")
            usr.init_system_handling(init_system, "start", "openvpn")
            
            print("[*] Looks like you are locked and loaded.\nNow, move your *.ovpn configuration file to your client and enjoy the freedom.")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def wireguard_server_setup(distro: str, init_system: str) -> None:
    system("clear")
    
    print("We are going to setup your server for Wireguard.")
    answer: str = input("\n[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            print("[<==] Updating the system...")
            usr.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing Wireguard...")
            usr.package_handling(distro, package_list=["wireguard", "wireguard-tools"], command="install")

            print("[<==] Installing Curl...")
            usr.package_handling(distro, package_list=["curl"], command="install")

            print("[<==] Installing Wireguard-Installer script...")
            ...
            sleep(1)

            print("[<==] Restarting Wireguard service && Finishing installation...")
            usr.init_system_handling(init_system, "start", "wireguard")

            print("[*] Looks like you are locked and loaded.\n (...)")
        except subprocess.CalledProcessError as error:
            print(f"{RED} Error: {error}{RESET}")


def outlinevpn_server_setup(distro: str, init_system: str) -> None:
    system("clear")

    print("We are going to setup your server for OutlineVPN.") 
    answer: str = input("\n[?] Proceed? (y/N): ")
    if answer in ["y", "yes"]:
        try:
            print("[<==] Updating the system...")
            usr.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing Docker...")
            subprocess.run(["wget", "-O", "https://get.docker.com", "|", "bash"], check=True, shell=True)

            print("[<==] Starting Docker...")
            usr.init_system_handling(init_system, "start", "docker")

            print("[*] Looks like you are locked and loaded.\nNow, check the instructions in Outline Manager.")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def vpn_server_setup() -> None:
    system("clear")

    functions: dict = {
            "openvpn_server_setup": openvpn_server_setup,
            "wireguard_server_setup": wireguard_server_setup,
            "outlinevpn_server_setup": outlinevpn_server_setup
            }

    print("+---- VPN Server Setup ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__":
    vpn_server_setup()
