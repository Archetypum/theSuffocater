#!/usr/bin/python3

"""
---------------------------------------
Reduces the risk of vulnerabilities being exploited and helps keep your system stable and secure.
Debian-Based GNU/Linux distributions only supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

import subprocess
from os import system


def enable_auto_updates() -> None:
    os.system("clear")

    print("Automatic updates help ensure your system is always protected with the latest security patches and improvements.")
    print("By enabling automatic updates, your system will regularly check for updates and install them without manual intervention.")
    print("This reduces the risk of vulnerabilities being exploited and helps keep your system stable and secure.")

    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        print("Enabling automatic updates...")
        subprocess.run(["apt", "update", "-y"], check=True)
        subprocess.run(["apt", "install", "unattended-upgrades", "-y"], check=True)
        subprocess.run(["dpkg-reconfigure", "-plow", "unattended-upgrades"], check=True)
       
        try:
            with open("config_files/auto_update_config.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/apt/apt.conf.d/20auto-upgrades", "w") as true_config_file:
                true_config_file.write(config_file_text)

            print("\nAutomatic updates have been enabled.")
        except FileNotFoundError:
            print("Configuration file not found.")
        except IOError as e:
            print(f"An IOError occurred: {e}")


def disable_auto_updates() -> None:
    os.system("clear")

    print("Disabling automatic updates will stop your system from automatically checking for and installing updates.")
    print("This may leave your system vulnerable to unpatched security issues.")

    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        print("Disabling automatic updates...")

        try:
            with open("config_files/disable_auto_update_config.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/apt/apt.conf.d/20auto-upgrades", "w") as true_config_file:
                true_config_file.write(config_file_text)

            print("\nAutomatic updates have been disabled.")
        except FileNotFoundError:
            print("Configuration file not found.")
        except IOError as e:
            print(f"An IOError occurred: {e}")


def auto_updates() -> None:
    system("clear")

    functions: dict = {
            "enable_auto_updates": enable_auto_updates,
            "disable_auto_updates": disable_auto_updates
            }

    print("+---- Auto Updates  ----+")
    print("\nAvaiable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("Enter function name (or anything to leave) >>> ").lower()
    if your_function in functions:
        functions[your_function]()
