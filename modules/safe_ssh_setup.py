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
        if distro in ["debian", "devuan", "ubuntu", "trisquel", "mint", "lmde"]:
            subprocess.run(["apt", "install", "openssh-client", "openssh-server", "-y"], check=True)
        elif distro in ["arch", "artix"]:
            subprocess.run(["pacman", "-S", "openssh", "--noconfirm"], check=True)
        elif distro == "freebsd":
            subprocess.run(["pkg", "install", "openssh"], check=True)
        else:
            print(f"Unsupported distribution: {distro}")
            return

        try:
            with open("config_files/secure_ssh_config.txt", "r") as config_file:
                secure_ssh_config_text = config_file.read()
        except FileNotFoundError:
            print("Configuration file 'config_files/secure_ssh_config.txt' not found.")
            return
        except IOError as e:
            print(f"An error occurred while reading the config file: {e}")
            return

        try:
            with open("/etc/ssh/sshd_config", "w") as true_config_file:
                true_config_file.write(secure_ssh_config_text)
        except IOError as e:
            print(f"An error occurred while writing to /etc/ssh/sshd_config: {e}")
            return

        if init_system == "sysvinit":
            subprocess.run(["service", "ssh", "restart"], check=True)
            print("\nSuccess! SSH service restarted.")
        elif init_system == "systemd":
            subprocess.run(["systemctl", "enable", "sshd"], check=True)
            subprocess.run(["systemctl", "start", "sshd"], check=True)
            print("\nSuccess! SSH service started and enabled.")
        else:
            print("Unsupported init system.")
            return

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a subprocess: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_init_system() -> str:
    try:
        subprocess.check_output(["systemctl"], stderr=subprocess.STDOUT, text=True)
        return "systemd"
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError:
        pass

    try:
        subprocess.check_output(["service", "--help"], stderr=subprocess.STDOUT, text=True)
        return "sysvinit"
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError:
        pass

    return ""


def get_user_distro() -> str:
    try:
        with open("/etc/os-release") as release_file:
            for line in release_file:
                if line.startswith("ID="):
                    name: str = line.split("=")[1].strip().lower()
                    return name
    except FileNotFoundError:
        print("Cannot detect distribution from /etc/os-release.")
    
    name: str = input("Could you write the base of your OS yourself? (debian, arch, freebsd, etc.): ").strip().lower()
    return name


def safe_ssh_setup() -> None:
    system("clear")

    distro = get_user_distro()
    init_system = get_init_system()

    if not distro or not init_system:
        print("Failed to detect distribution or init system. Exiting.")
        exit(1)

    print("After running this module, the following changes will be made:")
    print("0. Install openssh-client and openssh-server.")
    print("1. Remove password authentication.")
    print("2. Add Pubkey authentication.")
    print("3. Permit root login.")
    print("4. Set MaxAuthTries to 3.")
    print("*. Many more.")

    answer = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        main(distro, init_system)
    else:
        print("Operation canceled.")
        exit(0)


if __name__ == "__main__":
    safe_ssh_setup()
