#!/usr/bin/python3

"""
---------------------------------------
Changes system MAC-Address and local IP.
GNU/Linux supported and BSD supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

try:
    import os
    import usr
    import random
    import subprocess
    from sys import exit
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")
    exit(1)


def get_valid_interfaces() -> list:
    try:
        interfaces: list = os.listdir("/sys/class/net")
        valid_interfaces: list = [interface for interface in interfaces if os.path.islink(f"/sys/class/net/{interface}")]
        return valid_interfaces
    except FileNotFoundError:
        print(f"{RED}[!] Error: /sys/class/net directory not found.{RESET}")
        return []


def change_mac() -> None:
    os.system("clear")

    print("We are going to change the system's MAC address.")
    if not usr.prompt_user("[?] Proceed?"):
        print(f"{RED}[!] Operation canceled.{RESET}")
        return

    interfaces: list = get_valid_interfaces()
    if not interfaces:
        print(f"{RED}[!] No valid interfaces found. Exiting.{RESET}")
        return

    print(f"Available interfaces: {interfaces}")
    interface: str = input("\n[==>] Enter your interface: ").strip()

    if interface not in interfaces:
        print(f"{RED}[!] Invalid interface. Exiting.{RESET}")
        return

    new_mac: str = input("[==>] Enter new MAC-address [automatic]: ")
    if new_mac == "":
        mac_parts: list = [random.randint(0, 255) for _ in range(6)]
        new_mac: str = ":".join(f"{part:02x}" for part in mac_parts)
        print(f"[*] Your new MAC address: {new_mac}")

    try:
        subprocess.run(["ifconfig", interface, "down"], check=True)
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        
        print(f"\n{GREEN}[*] Success! MAC address changed.{RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"{RED}[!] Error while changing MAC address:\n{error}{RESET}")


def change_lan_ip() -> None:
    os.system("clear")
    
    print("We are going to change the local IP address.")
    if not usr.prompt_user("[?] Proceed?"):
        print(f"{RED}[!] Operation canceled.{RESET}")
        return

    interfaces: list = get_valid_interfaces()
    if not interfaces:
        print(f"{RED}[!] No valid interfaces found. Exiting.{RESET}")
        return

    print(f"Available interfaces: {interfaces}")
    interface: str = input("\n[==>] Enter your interface: ").strip()

    if interface not in interfaces:
        print(f"{RED}[!] Invalid interface. Exiting.{RESET}")
        return

    new_ip: str = input("[==>] Enter new IP address (e.g., 192.168.1.10): ").strip()
    if new_ip == "":
        new_ip: str = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        print(f"[*] Your new IP address: {new_ip}")
    if not is_valid_ip(new_ip):
        print(f"{RED}[!] Error: Invalid IP address: {new_ip}. Exiting.{RESET}")
        return

    subnet_mask: str = input("[==>] Enter subnet mask (e.g., 255.255.255.0): ").strip()
    if subnet_mask == "":
        subnet_mask: str = "255.255.255.0"
    if not is_valid_ip(subnet_mask):
        print(f"{RED}[!] Error: Invalid subnet mask: {subnet_mask}{RESET}")
        return

    try:
        subprocess.run(["ip", "addr", "flush", "dev", interface], check=True)
        subprocess.run(["ip", "addr", "add", f"{new_ip}/{subnet_mask}", "dev", interface], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        print(f"\n{GREEN}[*] Success! IP address changed.{RESET}")
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"{RED}[!] Error: cant change IP address: {error}.{RESET}")
        print("[*] We will try another way...") 
        try:
            subprocess.run(["ifconfig", interface, "inet", new_ip, "netmask", subnet_mask], check=True)
            print(f"\n{GREEN}[*] Success! IP address changed.{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            print(f"{RED}[!] Error: still cant change IP address: {error}.{RESET}")
            

def address_management() -> None:
    os.system("clear")

    functions: dict = {
        "change_mac": change_mac,
        "change_lan_ip": change_lan_ip
    }

    print("+---- Address Management ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name: ").lower()
    if your_function in functions:
        functions[your_function]()
