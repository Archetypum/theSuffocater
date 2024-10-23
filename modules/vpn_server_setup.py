#!/usr/bin/python3

"""
---------------------------------------
Setup your VPN servers automaticly with this module.
GNU/Linux and BSD supported (OpenVPN, Wireguard)
GNU/Linux supported (OutlineVPN)

Author: iva
Date: 18.10.2024
---------------------------------------
"""

import subprocess
from os import system
from time import sleep


def openvpn_server_setup() -> None:
    system("clear")
    ...


def wireguard_server_setup() -> None:
    system("clear")
    ...


def outlinevpn_server_setup() -> None:
    system("clear")

    print("We are going to setup your server for OutlineVPN.")
    
    answer: str = input("\nAre you sure you want this? (y/n): ")
    if answer in ["y", "yes"]:
        try:
            print("Updating the system...")
            subprocess.run(["apt", "update", "&&", "apt", "upgrade", "-y"], check=True, shell=True)
            sleep(1)

            print("Installing Docker...")
            subprocess.run(["wget", "-O", "https://get.docker.com", "|", "bash"], check=True, shell=True)
            sleep(1)

            print("Starting Docker...")
            subprocess.run(["service", "docker", "start"], check=True, shell=True)
            sleep(1)
            
            print("Installing Iptables for future...")
            subprocess.run(["apt", "install", "iptables", "-y"], check=True, shell=True)
            sleep(1)

            print("Looks like you are locked and loaded.\nNow, check the instructions in Outline Manager.")
        
        except subprocess.CalledProcessError as e:
            print(f"An error occured: {e}")


def vpn_server_setup() -> None:
    system("clear")

    functions: dict = {
            "openvpn_server_setup": openvpn_server_setup,
            "wireguard_server_setup": wireguard_server_setup,
            "outlinevpn_server_setup": outline_vpn_server_setup
            }

    print("+---- VPN Server Setup ----+")
    print("\nAvaiable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("Enter function name (or anything to leave) >>> ").lower()
    if your_function in functions:
        functions[your_function]()
