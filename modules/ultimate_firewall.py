#!/usr/bin/python3

"""
---------------------------------------
Setups firewalls for you using pre-build profiles.
GNU/Linux and BSD supported.

Author: iva
Date: 09.11.2024
---------------------------------------
"""

try:
    import os
    import usr
    import subprocess
    from sys import exit
    from typing import List
    from os import system, listdir
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")
    exit(1)


def toggle_interfaces(state: str, interfaces: List[str]) -> None:
    for interface in interfaces:
        try:
            subprocess.run(["ifconfig", interface, state], check=True)
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error with interface {interface}: {error}{RESET}")
            raise


def toggle_bsd_firewall(enable: bool) -> None:
    action: str = "e" if enable else "d"
    try:
        subprocess.run(["pfctl", f"-{action}"], check=True)
        action_str: str = "accept_all" if enable else "block_all"
        subprocess.run(["pfctl", "-f", "/etc/pf.conf", "-a", action_str, "pass all" if enable else "block all"], check=True)
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] error: {error}{RESET}")
        raise


def toggle_gnulinux_firewall(enable: bool) -> None:
    action: str = "ACCEPT" if enable else "DROP"
    try:
        subprocess.run(["iptables", "-P", "INPUT", action], check=True)
        subprocess.run(["iptables", "-P", "OUTPUT", action], check=True)
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error: {error}{RESET}")
        raise


def drop_firewall() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    bsd_distros: list = [usr.FREEBSD_BASED_DISTROS, usr.OPENBSD_BASED_DISTROS, usr.NETBSD_BASED_DISTROS]
    interfaces: list = ["wlan0", "eth0"]

    try:
        if distro in bsd_distros:
            print("[<==] Disabling radio (if supported by system)...")
            toggle_interfaces("down", interfaces)

            print("[<==] Blocking all input/output traffic...")
            toggle_bsd_firewall(enable=False)
        else:
            print("[<==] Stopping radio...")
            toggle_interfaces("down", interfaces)
            subprocess.run(["nmcli", "radio", "all", "off"], check=True)

            print("[<==] Disabling input/output traffic...")
            toggle_gnulinux_firewall(enable=False)

        print(f"{GREEN}[*] Success!{RESET}")
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error: {error}{RESET}")


def accept_firewall() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    bsd_distros: list = [usr.FREEBSD_BASED_DISTROS, usr.OPENBSD_BASED_DISTROS, usr.NETBSD_BASED_DISTROS]
    interfaces: list = ["wlan0", "eth0"]

    try:
        if distro in bsd_distros:
            print("[<==] Enabling radio (if supported by system)...")
            toggle_interfaces("up", interfaces)

            print("[<==] Enabling input/output traffic...")
            toggle_bsd_firewall(enable=True)
        else:
            print("[<==] Enabling radio...")
            subprocess.run(["nmcli", "radio", "all", "on"], check=True)

            print("[<==] Enabling input/output traffic...")
            toggle_gnulinux_firewall(enable=True)

        print(f"{GREEN}[*] Success!{RESET}")
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error: {error}{RESET}")



def iptables_setup() -> None:
    system("clear")

    print("We are going to set up basic iptables rules to secure your machine.")
    answer: str = input("[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        interfaces: str = listdir("/sys/class/net")
        print(f"Interfaces:\n{[interface for interface in interfaces if os.path.islink(f'/sys/class/net/{interface}')]}")
        interface: str = input("\n[==>] Enter your interface: ")

        rules: list = [
            ("Loopback", ["lo"], ["lo"]),
            ("Ping", ["icmp"], ['icmp']),
            ("Web", ["80", "443"], ["80", "443"]),
            ("DNS", ["53"], ["53"]),
            ("NTP", ["123"], ["123"]),
            ("CUPS", ["631"], ["631"]),
            ("SSH", ["22"], ["22"]),
            ("DHCP", ["67:68"], ["67:68"])
        ]
        
        for rule_name, input_ports, output_ports in rules:
            choice: str = input(f"\n[?] Allow {rule_name}? (y/N): ").lower()
            if choice in ["y", "yes"]:
                for port in input_ports:
                    subprocess.run(["iptables", "-A", "INPUT", "-i", interface, "-p", "tcp", "--dport", port, "-j", "ACCEPT"], check=True)
                for port in output_ports:
                    subprocess.run(["iptables", "-A", "OUTPUT", "-o", interface, "-p", "tcp", "--dport", port, "-j", "ACCEPT"], check=True)

        reject_choice: str = input("\n[?] Reject everything else that was not explicitly allowed? (y/N): ").lower()
        if reject_choice in ["y", "yes"]:
            subprocess.run(["iptables", "-A", "INPUT", "-j", "REJECT"], check=True)
            subprocess.run(["iptables", "-A", "OUTPUT", "-j", "REJECT"], check=True)

        print(f"{GREEN}[*] Success!{RESET}")


def block_ip_addresses(ip_addresses: list) -> None:
    try:
        for ip in ip_addresses:
            subprocess.run(["pfctl", "-t", "blocklist", "-T", "add", ip], check=True)
        print(f"{GREEN}[*] IPs successfully blocked with pfctl.{RESET}")
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error while blocking IPs using pfctl: {error}{RESET}")


def handle_ufw(ip_addresses: list, action: str, init_system: str) -> None:
    try:
        for ip in ip_addresses:
            subprocess.run(["ufw", action, "out", "from", ip], check=True)
            subprocess.run(["ufw", action, "out", "to", ip], check=True)
        
        subprocess.run(["ufw", "enable"], check=True)
        usr.init_system_handling(init_system, "start", "ufw")
        subprocess.run(["ufw", "reload"], check=True)
        print(f"{GREEN}[*] Success!{RESET}")
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error while executing UFW {action}: {error}{RESET}")


def no_spying() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    bsd_distros: list = [usr.FREEBSD_BASED_DISTROS, usr.OPENBSD_BASED_DISTROS, usr.NETBSD_BASED_DISTROS]
    ip_addresses: list = [
        "91.207.136.55",    # starvapol_datacenter_ip
        "20.54.36.64",      # dublin_microsoft_ip
        "64.233.163.99",    # london_google_ip
        "34.107.221.82",    # kansas_google_ip
        "34.149.100.209",   # kansas_google_ip2
        "142.250.74.42",    # stockholm_google_ip
        "35.224.181.201",   # councilbluffs_google_ip
        "162.159.61.4",     # sanfrancisco_cloudflare_ip
        "104.26.10.222",    # sanfrancisco_cloudflare_ip2
        "54.243.196.140",   # ashburn_amazon_ip
        "3.217.123.24",     # ashburn_amazon_ip2
        "3.164.68.27",      # seattle_amazon_ip
        "3.164.240.75",     # seattle_amazon_ip2
        "3.164.240.98",     # stockholm_amazon_ip
        "93.243.107.34",    # brandenburg_telekom_ip
        "209.100.149.34",   # london_datacenter_ip
        "40.114.178.124",   # amsterdam_microsoft_ip
        "172.64.41.4",      # sanfrancisco_cloudflare_ip
        "93.243.107.34",    # brandenburg_telekom_ip
        "178.128.135.204",  # newjersey_datacenter_ip
        "82.221.107.34",    # reykjavik_datacenter_ip
        "104.19.222.79",    # sanfranciso_cloudflare_ip
        "104.21.42.32",     # sanfrancisco_cloudflare_ip
        "191.144.160.34",   # bolivar_datacenter_ip (the fuck?! columbia???)
        "104.18.32.115",    # sanfrancisco_cloudflare_ip
        "151.101.194.132"   # stockholm_datacenter_ip
    ]

    print(f"We are going to block {len(ip_addresses)} of big companies/datacenters/ISPs.")
    if usr.prompt_user("[?] Proceed?"):
        answer: str = input("[?] Reject or Deny? (r/D): ").lower()
        
        if answer in ["d", "deny", "r", "reject"]:
            if distro in bsd_distros:
                block_ip_addresses(ip_addresses)
            
            if answer in ["d", "deny"]:
                handle_ufw(ip_addresses, "deny", init_system)
            elif answer in ["r", "reject"]:
                handle_ufw(ip_addresses, "reject", init_system)


def porter() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    active_ports: bytes = subprocess.check_output(["lsof", "-i", "-P", "-n", "|", "grep", "LISTEN"], shell=True)
    bsd_distros: list = [usr.FREEBSD_BASED_DISTROS, usr.OPENBSD_BASED_DISTROS, usr.NETBSD_BASED_DISTROS]

    print(f"\nActive listening ports:\n{active_ports.strip().decode()}")
    answer: str = input("[?] Open/Close ports? (Open/Close): ").lower()
    if answer in ["o", "open"]:
        port: str = input("[==>] Enter the port number you want to open: ")
        while not port.isdigit() or not (1 <= int(port) <= 65535):
            port: str = input("[==>] Enter a valid port number (1-65535): ")
        
        try:
            if distro in bsd_distros:
                subprocess.run(["pfctl", "-f", "/etc/pf.conf", "-a", f"port_open_{port}", f"pass in on any proto tcp from any to any port {port}"], check=True)
                print(f"{GREEN}[*] Port {port} has been opened.{RESET}")
            else:
                subprocess.run(["ufw", "allow", port], check=True)
                print(f"{GREEN}[*] Port {port} has been opened.{RESET}")
        except (subprocess.CalledProcessError, ValueError) as error:
            print(f"{RED}[!] Failed to open port {port}:\n{error}{RESET}")

    elif answer in ["c", "close"]:
        port: str = input("[==>] Enter the port number you want to close: ")
        while not port.isdigit() or not (1 <= int(port) <= 65535):
            port: str = input("[==>] Enter a valid port number (1-65535): ")
        try:
            if distro in bsd_distros:
                subprocess.run(["pfctl", "-f", "/etc/pf.conf", "-a", f"port_close_{port}", f"block in on any proto tcp from any to any port {port}"], check=True)
                print(f"{GREEN}[*] Port {port} has been closed using pfctl.{RESET}")
            else:
                subprocess.run(["ufw", "deny", port], check=True)
                print(f"{GREEN}[*] Port {port} has been closed.{RESET}")
        except (subprocess.CalledProcessError, ValueError) as error:
            print(f"{RED}[!] Error: Failed to close port {port}:\n{error}{RESET}")


def ultimate_firewall() -> None:
    system("clear")

    profiles: dict = {
            "drop_all": drop_firewall,
            "accept_all": accept_firewall,
            "no_spying": no_spying,
            "iptables_setup": iptables_setup,
            "porter": porter
            }

    print("+---- Ultimate Firewall ----+")
    print("\nAvailable Profiles:")
    for profile in profiles.keys():
        print(f" - {profile}")
    
    your_profile: str = input("[==>] Enter function name: ")
    if your_profile in profiles:
        profiles[your_profile]()


if __name__ == "__main__":
    ultimate_firewall()
