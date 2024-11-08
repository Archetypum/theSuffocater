#!/usr/bin/python3

"""
---------------------------------------
Hardens your SSH by configuring the sshd_config file. Essential to your server!
GNU/Linux and BSD supported.

Author: iva
Date: 03.07.2024
---------------------------------------
"""

import subprocess
from sys import exit
from os import system


def main(distro: str, init_system: str) -> None:
    try:
        if distro == "debian":
            subprocess.run(["apt", "install", "openssh-client", "openssh-server", "-y"], check=True, shell=True)
        elif distro == "arch":
            subprocess.run(["pacman", "-S", "openssh", "--noconfirm"], check=True, shell=True)
        elif distro == "freebsd":
            subprocess.run(["pkg", "install", "openssh"], check=True, shell=True)
        else:
            print("Unsupported disto.")

        with open("config_files/secure_ssh_config.txt", "r") as config_file:
            secure_ssh_config_text: str = config_file.read()

        with open("/etc/ssh/sshd_config", "w") as true_config_file:
            true_config_file.write(secure_ssh_config_text)
        
        if init_system == "sysvinit":
            subprocess.run(["service", "ssh", "restart"], check=True, shell=True)
            print("\nSuccess!")
        elif init_system == "systemd":
            subprocess.run(["systemctl", "enable", "sshd"], check=True, shell=True)
            subprocess.run(["systemctl", "start", "sshd"], check=True, shell=True)
        else:
            print("Unsupported distro.")

    except FileNotFoundError:
        print("Configuration file not found.")
    except IOError as e:
        print(f"An IOError occurred: {e}")


def get_init_system() -> str:
    try:
        output: str = subprocess.check_output(["systemctl"], stderr=subprocess.STDOUT, text=True)
        if "systemd" in output:
            return "systemd"
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError:
        pass

    try:
        output: str = subprocess.check_output(["service", "--help"], stderr=subprocess.STDOUT, text=True)
        if "Usage: service" in output:
            return "sysvinit"
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError:
        pass


def get_user_distro() -> str:
    try:
        with open("/etc/os-release") as release_file:
            for line in release_file:
                if line.startswith("ID_LIKE="):
                    name: str = line.split("=")[1]
                    return name
    except FileNotFoundError:
        print("Cant get your distribution name,")
        name: str = input("Could you write the base of your OS yourself? (debian, arch, freebsd, etc.): ")
        return name


def safe_ssh_setup() -> None:
    system("clear")

    distro: str = get_user_distro()
    init_system: str = get_init_system()

    print("After running this module, the following changes will be made:")
    print("0. Install openssh-client and openssh-server;")
    print("1. Remove password authentication;")
    print("2. Add Pubkey authentication;")
    print("3. Permit root login;")
    print("4. Set MaxAuthTries to 6.")

    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        main(distro, init_system)
