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
from os import system


def safe_ssh_setup() -> None:
    system("clear")

    print("After running this module, the following changes will be made:")
    print("1. Remove password authentication;")
    print("2. Add Pubkey authentication;")
    print("3. Permit root login;")
    print("4. Set MaxAuthTries to 6.")

    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        try:
            with open("config_files/secure_ssh_config.txt", "r") as config_file:
                secure_ssh_config_text: str = config_file.read()

            with open("/etc/ssh/sshd_config", "w") as true_config_file:
                true_config_file.write(secure_ssh_config_text)

            subprocess.run(["service", "ssh", "restart"], check=True)
            print("\nSuccess!")
        except FileNotFoundError:
            print("Configuration file not found.")
        except IOError as e:
            print(f"An IOError occurred: {e}")
