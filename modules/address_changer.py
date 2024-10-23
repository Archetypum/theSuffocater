#!/usr/bin/python3

"""
---------------------------------------
Can change system's MAC-Address and local IP.
GNU/Linux supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

import re
import os
import random
import subprocess


def change_mac() -> None:
    os.system("clear")
    print("We are going to change the system's MAC-Address.")

    answer: str = input("Are you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        try:
            interfaces: list = os.listdir("/sys/class/net")
            print(f"Interfaces:\n{[interface for interface in os.listdir('/sys/class/net') if os.path.islink(f'/sys/class/net/{interface}')]}")
            interface: str = input("\nEnter your interface: ")

            mac_parts: list = [random.randint(0, 255) for _ in range(6)]
            new_mac: str = ":".join(f"{part:02x}" for part in mac_parts)

            print(f"Your new MAC-Address: {new_mac}")
            subprocess.run(["ifconfig", interface, "down"], check=True)
            subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], check=True)
            subprocess.run(["ifconfig", interface, "up"], check=True)

            print("\nSuccess!")
        except subprocess.CalledProcessError as e:
            print(e)


def change_lan_ip() -> None:
    os.system("clear")
    print("We are going to change the local IP address.")
    
    answer: str = input("Are you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        interfaces: list = os.listdir("/sys/class/net")
        valid_interfaces = [interface for interface in interfaces if os.path.islink(f"/sys/class/net/{interface}")]
    
        print(f"Available Interfaces: {valid_interfaces}")
        interface: str = input("\nEnter your interface: ")

        if interface not in valid_interfaces:
            print("Invalid interface. Exiting.")
            return

        new_ip: str = input("Enter the new IP address (e.g., 192.168.1.10): ")
        subnet_mask: str = input("Enter the subnet mask (e.g., 255.255.255.0): ")

        try:
            subprocess.run(["ip", "addr", "flush", "dev", interface], check=True)
            subprocess.run(["ip", "addr", "add", f"{new_ip}/{subnet_mask}", "dev", interface], check=True)
            subprocess.run(["ip", "link", "set", interface, "up"], check=True)

            print("\nSuccess! IP Address changed.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")


def address_changer() -> None:
    os.system("clear")

    functions: dict = {
            "change_mac": change_mac,
            "change_lan_ip": change_lan_ip
            }

    print("+---- Address Changer ----+")
    print("\nAvaiable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("Enter function name (or anything to leave) >>> ").lower()
    if your_function in functions:
        functions[your_function]()
