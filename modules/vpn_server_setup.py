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
from sys import exit
from os import system
from time import sleep


def openvpn_server_setup(init_system: str) -> None:
    system("clear")

    print("We are going to setup your server for OpenVPN.")

    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        try:
            print("Updating the system...")
            subprocess.run(["apt", "update", "&&", "apt", "upgrade", "-y"], check=True, shell=True)
            sleep(1)

            print("Installing OpenVPN...")
            subprocess.run(["apt", "install", "openvpn", "-y"], check=True, shell=True)
            sleep(1)

            print("Installing Curl...")
            subprocess.run(["apt", "install", "curl", "-y"], check=True, shell=True)
            sleep(1)
            
            print("Installing OpenVPN-Installer script...")
            subprocess.run(["curl", "-LJO", "https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh"], check=True, shell=True)
            subprocess.run(["chmod", "+x", "openvpn-install.sh"], check=True, shell=True)
            subprocess.run(["./openvpn-install.sh"], check=True, shell=True)
            sleep(1)

            print("Installing Iptables for future...")
            subprocess.run(["apt", "install", "iptables", "-y"], check=True, shell=True)
            sleep(1)
            
            print("Finishing installation...")
            if init_system == "sysvinit":
                subprocess.run(["service", "openvpn", "restart"], check=True, shell=True)
            else:
                subprocess.run(["systemctl", "restart", "openvpn"], check=True, shell=True)
            sleep(1)

            print("Looks like you are locked and loaded.\nNow, move your *.ovpn configuration file to your client and enjoy the freedom.")
        except subprocess.CalledProcessError as e:
            print(f"An error occured: {e}")


def wireguard_server_setup(init_system: str) -> None:
    system("clear")
    
    print("We are going to setup your server for Wireguard.")
    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        try:
            ...
        except subprocess.CalledProcessError as e:
            print(f"An error occured: {e}")


def outlinevpn_server_setup(init_system: str) -> None:
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


def detect_init_system():
    try:
        output = subprocess.check_output(["systemctl"], stderr=subprocess.STDOUT, text=True)
        if "systemd" in output:
            return "systemd"
    except FileNotFoundError:
        pass
    except subprocess.CalledProcessError:
        pass

    try:
        output = subprocess.check_output(["service", "--help"], stderr=subprocess.STDOUT, text=True)
        if "Usage: service" in output:
            return "sysvinit"
    except subprocess.CalledProcessError:
        pass

    print("This module does not support your init system.")
    return None


def vpn_server_setup() -> None:
    system("clear")

    init_system = detect_init_system()
    functions: dict = {
            "openvpn_server_setup": openvpn_server_setup,
            "wireguard_server_setup": wireguard_server_setup,
            "outlinevpn_server_setup": outlinevpn_server_setup
            }

    print("+---- VPN Server Setup ----+")
    print("\nAvaiable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("Enter function name (or anything to leave) >>> ").lower()
    if your_function in functions:
        functions[your_function](init_system)
