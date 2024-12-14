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
    from os import system, listdir
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")
    exit(1)


def drop_firewall() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()

    try:
        if distro in usr.FREEBSD_BASED_DISTROS or distro in usr.OPENBSD_BASED_DISTROS or distro in usr.NETBSD_BASED_DISTROS:
            print("[<==] Disabling radio (if supported by system)...")
            subprocess.run(["ifconfig", "wlan0", "down"], check=True)
            subprocess.run(["ifconfig", "eth0", "down"], check=True)
            
            print("[<==] Blocking all input/output traffic...")
            subprocess.run(["pfctl", "-d"], check=True)
            subprocess.run(["pfctl", "-f", "/etc/pf.conf", "-a", "block_all", "block all"], check=True)
        else:
            print("[<==] Stopping radio...")
            subprocess.run(["ifconfig", "wlan0", "down"], check=True)
            subprocess.run(["ifconfig", "eth0", "down"], check=True)
            subprocess.run(["nmcli", "radio", "all", "off"], check=True)

            print("[<==] Disabling input/output traffic...")
            subprocess.run(["iptables", "-P", "INPUT", "DROP"], check=True)
            subprocess.run(["iptables", "-P", "OUTPUT", "DROP"], check=True)

        print(f"{GREEN}[*] Success!{RESET}")
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error: {error}{RESET}")


def accept_firewall() -> None:
    system("clear")
    distro: str = usr.get_user_distro()

    try:
        if distro in usr.FREEBSD_BASED_DISTROS or distro in usr.OPENBSD_BASED_DISTROS or distro in usr.NETBSD_BASED_DISTROS:
            print("[<==] Enabling radio (if supported by system)...")
            subprocess.run(["ifconfig", "wlan0", "up"], check=True)

            print("[<==] Enabling input/output traffic...")
            subprocess.run(["pfctl", "-e"], check=True)
            subprocess.run(["pfctl", "-f", "/etc/pf.conf", "-a", "accept_all", "pass all"], check=True)
        else:
            print("[<==] Enabling radio...")
            subprocess.run(["nmcli", "radio", "all", "on"], check=True)

            print("[<==] Enabling input/output traffic...")
            subprocess.run(["iptables", "-P", "INPUT", "ACCEPT"], check=True)
            subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"], check=True)

        print(f"{GREEN}[*] Success!{RESET}")
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error: {error}{RESET}")


def iptables_setup() -> None:
    system("clear")

    print("We are going to set up basic iptables rules to secure your machine.")
    answer: str = input("[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        interfaces = listdir("/sys/class/net")
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
                    subprocess.run(f"iptables -A INPUT -i {interface} -p tcp --dport {port} -j ACCEPT", check=True)
                for port in output_ports:
                    subprocess.run(f"iptables -A OUTPUT -o {interface} -p tcp --dport {port} -j ACCEPT", check=True)

        reject_choice: str = input("\n[?] Reject everything else that was not explicitly allowed? (y/N): ").lower()
        if reject_choice in ["y", "yes"]:
            subprocess.run(["iptables", "-A", "INPUT", "-j", "REJECT"], check=True)
            subprocess.run(["iptables", "-A", "OUTPUT", "-j", "REJECT"], check=True)

        print(f"{GREEN}[*] Success!{RESET}")


def no_spying() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
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
            if distro in usr.FREEBSD_BASED_DISTROS or distro in usr.OPENBSD_BASED_DISTROS or distro in usr.NETBSD_BASED_DISTROS:
                try:
                    for ip in ip_addresses:
                        subprocess.run(["pfctl", "-t", "blocklist", "-T", "add", ip], check=True)
                    print(f"{GREEN}[*] Success!{RESET}")
                except subprocess.CalledProcessError as error:
                    print(f"{RED}[!] Error: {error}{RESET}")
            
            if answer in ["d", "deny"]:
                try:
                    for ip in ip_addresses:
                        subprocess.run(["ufw", "deny", "out", "from", ip], check=True)
                        subprocess.run(["ufw", "deny", "out", "to", ip], check=True)
                    
                    subprocess.run(["ufw", "enable"], check=True)
                    usr.init_system_handling(init_system, "start", "ufw")
                    subprocess.run(["ufw", "reload"], check=True)
                    
                    print(f"{GREEN}[*] Success!{RESET}")
                except subprocess.CalledProcessError as error:
                    print(f"{RED}[!] Error: {error}{RESET}")
            
            elif answer in ["r", "reject"]:
                try:
                    for ip in ip_addresses:
                        subprocess.run(["ufw", "reject", "out", "from", ip], check=True)
                        subprocess.run(["ufw", "reject", "out", "to", ip], check=True)
                    
                    subprocess.run(["ufw", "enable"], check=True)
                    usr.init_system_handling(init_system, "start", "ufw")
                    subprocess.run(["ufw", "reload"], check=True)
                    
                    print(f"{GREEN}[*] Success!{RESET}")
                except subprocess.CalledProcessError as error:
                    print(f"{RED}[!] Error: {error}{RESET}")


def porter() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    active_ports: bytes = subprocess.check_output("lsof -i -P -n | grep LISTEN", shell=True).strip()
    
    print(f"\nActive listening ports:\n{active_ports}")
    answer: str = input("[?] Open/Close ports? (Open/Close): ").lower()
    if answer in ["o", "open"]:
        port: str = input("[==>] Enter the port number you want to open: ")
        try:
            if distro in usr.FREEBSD_BASED_DISTROS or distro in usr.OPENBSD_BASED_DISTROS or distro in usr.NETBSD_BASED_DISTROS:
                subprocess.run(["pfctl", "-f", "/etc/pf.conf", "-a", f"port_open_{port}", f"pass in on any proto tcp from any to any port {port}"], check=True)
                print(f"{GREEN}[*] Port {port} has been opened.{RESET}")
            else:
                subprocess.run(["ufw", "allow", port], check=True)
                print(f"{GREEN}[*] Port {port} has been opened.{RESET}")
        except (subprocess.CalledProcessError, ValueError) as error:
            print(f"{RED}[!] Failed to open port {port}:\n{error}{RESET}")

    elif answer in ["c", "close"]:
        port: str = input("[==>] Enter the port number you want to close: ")
        try:
            if distro in usr.FREEBSD_BASED_DISTROS or distro in usr.OPENBSD_BASED_DISTROS or distro in usr.NETBSD_BASED_DISTROS:
                subprocess.run(["pfctl", "-f", "/etc/pf.conf", "-a", f"port_close_{port}", f"block in on any proto tcp from any to any port {port}"], shell=True)
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
