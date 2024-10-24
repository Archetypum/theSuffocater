#!/usr/bin/python3

"""
---------------------------------------
Setups firewalls for you using pre-build profiles.
GNU/Linux and BSD supported.

Author: iva
Date: 09.11.2024
---------------------------------------
"""

import subprocess
from os import system


def drop_firewall() -> None:
    system("clear")
    print("Stopping radio...")
    subprocess.run(["nmcli", "radio", "all", "off"], check=True)
    
    print("Disabling input/output traffic...")
    subprocess.run(["iptables", "-P", "INPUT", "DROP"], check=True)
    subprocess.run(["iptables", "-P", "OUTPUT", "DROP"], check=True)
    

def accept_firewall() -> None:
    system("clear")
    print("Enabling radio...")
    subprocess.run(["nmcli", "radio", "all", "off"], check=True)
    
    print("Disabling input/output traffic...")
    subprocess.run(["iptables", "-P", "INPUT", "ACCEPT"], check=True)
    subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"], check=True)


def no_spying() -> None:
    system("clear")
    ip_addresses: list[str] = [
            '91.207.136.55',    # starvapol_datacenter_ip
            '20.54.36.64',      # dublin_microsoft_ip
            '64.233.163.99',    # london_google_ip
            '34.107.221.82',    # kansas_google_ip
            '34.149.100.209',   # kansas_google_ip2
            '142.250.74.42',    # stockholm_google_ip
            '35.224.181.201',   # councilbluffs_google_ip
            '162.159.61.4',     # sanfrancisco_cloudflare_ip
            '104.26.10.222',    # sanfrancisco_cloudflare_ip2
            '54.243.196.140',   # ashburn_amazon_ip
            '3.217.123.24',     # ashburn_amazon_ip2
            '3.164.68.27',      # seattle_amazon_ip
            '3.164.240.75',     # seattle_amazon_ip2
            '3.164.240.98',     # stockholm_amazon_ip
            '93.243.107.34',    # brandenburg_telekom_ip
            '209.100.149.34',   # london_datacenter_ip
            '40.114.178.124',   # amsterdam_microsoft_ip
            '172.64.41.4',      # sanfrancisco_cloudflare_ip
            '93.243.107.34',    # brandenburg_telekom_ip
            '178.128.135.204',  # newjersey_datacenter_ip
            '82.221.107.34',    # reykjavik_datacenter_ip
            '104.19.222.79',    # sanfranciso_cloudflare_ip
            '104.21.42.32',     # sanfrancisco_cloudflare_ip
            '191.144.160.34',   # bolivar_datacenter_ip (the fuck?! columbia???)
            '104.18.32.115',    # sanfrancisco_cloudflare_ip
            '151.101.194.132'   # stockholm_datacenter_ip
            ]

    print(f"We are going to block {len(ip_addresses)} of big companies/datacenters/isps by using UFW.")

    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        for ip in ip_addresses:
            subprocess.run(f"ufw deny from {ip} to any", check=True)
            subprocess.run(f"ufw deny out to {ip}", check=True)
            # subprocess.run(f"ufw reject from {ip}", check=True)
            # subprocess.run(f"ufw reject out to {ip}", check=True)

        subprocess.run("ufw enable", shell=True)
        subprocess.run("ufw reload", shell=True)
        subprocess.run("service ufw start", shell=True)
        subprocess.run("ufw status", shell=True)

        print("\nSuccess!")


def iptables_setup() -> None:
    system("clear")
    print("We are going to setup basic iptables rules to secure your machine.")

    answer: str = input("\nAre you sure you want this? (y/n): ").lower()
    if answer in ['y', 'yes']:
        interfaces: list = os.listdir('/sys/class/net')
        print(f"Interfaces:\n{[interface for interface in os.listdir('/sys/class/net') if os.path.islink(f'/sys/class/net/{interface}')]}")
        interface: str = input('\nEnter your interface: ')

        choice: str = input("\nHIGHLY RECOMMENDED!! Allow Loopback? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(['iptables', '-A', 'INPUT', '-i', 'lo', '-j', 'ACCEPT'], check=True)
            subprocess.run(['iptables', '-A', 'OUTPUT', '-o', 'lo', '-j', 'ACCEPT'], check=True)

        choice: str = input("\nAllow Ping? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "icmp", "-m", "state", "--state", "NEW", "--icmp-type", "8", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "icmp", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "icmp", "-j", "ACCEPT"], check=True, encoding='utf-8')

        choice: str = input("\nAllow connection to the Web? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "tcp", "-m", "state", "--state", "ESTABLISHED,RELATED", "--sport", "80", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "tcp", "-m", "state", "--state", "ESTABLISHED,RELATED", "--sport", "443", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "tcp", "-m", "tcp", "--dport", "80", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "tcp", "-m", "tcp", "--dport", "443", "-j", "ACCEPT"], check=True, encoding='utf-8')

        choice: str = input("\nHIGHLY RECOMMENDED!! Allow DNS? (y/n): ").lower()
        if choice in ['y', 'yes']:
            router_ip: str = input("\nEnter your router's IP (default gateway) to allow DNS connections: ")
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-s", router_ip, "-p", "udp", "--sport", "53", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-s", router_ip, "-p", "tcp", "--sport", "53", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-d", router_ip, "-p", "udp", "--dport", "53", "-m", "udp", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-d", router_ip, "-p", "tcp", "--dport", "53", "-m", "tcp", "-j", "ACCEPT"], check=True, encoding='utf-8')

        choice: str = input("\nAllow NTP to set and maintain the system time? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "udp", "-m", "state", "--state", "ESTABLISHED,RELATED", "--dport", "123", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "udp", "-m", "udp", "--sport", "123", "-j", "ACCEPT"], check=True, encoding='utf-8')

        choice: str = input("\nUnless you're using printer, allow CUPS connections? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(["iptables", "-A", "INPUT", "-p", "udp", "-m", "udp", "--dport", "631", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "INPUT", "-p", "tcp", "-m", "tcp", "--dport", "631", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-p", "udp", "-m", "udp", "--sport", "631", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-p", "tcp", "-m", "tcp", "--sport", "631", "-j", "ACCEPT"], check=True, encoding='utf-8')

        choice: str = input("\nEnable SSH? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "tcp", "-m", "state", "--state", "NEW,ESTABLISHED", "--dport", "22", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "tcp", "-m", "state", "--state", "ESTABLISHED", "--sport", "22", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "tcp", "-m", "state", "--state", "NEW,ESTABLISHED", "--dport", "22", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "tcp", "-m", "state", "--state", "ESTABLISHED", "--sport", "22", "-j", "ACCEPT"], check=True, encoding='utf-8')

        choice: str = input("\nHIGHLY RECOMMENDED!! Enable DHCP? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "udp", "-m", "state", "--state", "ESTABLISHED,RELATED", "--sport", "67:68", "-j", "ACCEPT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "udp", "-m", "udp", "--dport", "67:68", "-j", "ACCEPT"], check=True, encoding='utf-8')

        choice: str = input("\nReject everything else that you didn't explicitly allowed? (y/n): ").lower()
        if choice in ['y', 'yes']:
            subprocess.run(["iptables", "-A", "INPUT", "-j", "REJECT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "FORWARD", "-j", "REJECT"], check=True, encoding='utf-8')
            subprocess.run(["iptables", "-A", "OUTPUT", "-j", "REJECT"], check=True, encoding='utf-8')

        print("Successfully enabled iptables rules!")
        print("Dont forget to check your connectivity. Iptables can be a little tricky sometimes.")

        restore: str = input("\nIf you belive that something is wrong, enter RESTORE in capital letters: ")
        if restore == 'RESTORE':
            subprocess.run(["sudo", "iptables", "-F"], check=True)
            subprocess.run(["sudo", "iptables", "-X"], check=True)
            subprocess.run(["iptables", "-P", "INPUT", "ACCEPT"], check=True)
            subprocess.run(["iptables", "-P", "FORWARD", "ACCEPT"], check=True)
            subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"], check=True)
            print("Iptables are reset now. Re-check your connectivity.")

        print("\nSuccess!")


def porter() -> None:
    system("clear")

    active_ports: str = subprocess.check_output("lsof -i -P -n | grep LISTEN", shell=True).strip()
    print(f"\nActive listening ports:\n{active_ports}")

    answer: str = input("\nDo you want to open or close ports? (open/close): ").lower()
    if answer in ["o", "open"]:
        port: int = input("Enter the port number you want to open: ")
        try:
            subprocess.check_call(f"ufw allow {port}", shell=True)
            print(f"Port {port} has been opened.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to open port {port}: {e}")

    if answer in ["c", "close"]:
        port: int = input("Enter the port number you want to close: ")
        try:
            subprocess.check_call(f"ufw deny {port}", shell=True)
            print(f"Port {port} has been closed.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to close port {port}: {e}")


def ultimate_firewall() -> None:
    system("clear")

    profiles: dict = {
            "drop_all": drop_firewall,
            "accept_all": accept_firewall,
            "no_spying": no_spying,
            "iptables_setup": iptables_setup,
            "fail2ban_setup": fail2ban_setup,
            "porter": porter
            }

    print("+---- Ultimate Firewall ----+")
    print("\nAvaiable Profiles:")
    for profile in profiles.keys():
        print(f" - {profile}")
    
    while True:
        your_profile = input("\nEnter profile name (or anything to leave) >>> ")
        if your_profile in profiles:
            profiles[your_profile]()
