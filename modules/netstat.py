#!/usr/bin/python3

"""
---------------------------------------
Displays brief network statistics.
GNU/Linux and BSD supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

import socket
import requests
import subprocess
from os import system


def netstat() -> None:
    system("clear")
	basic_netstat: str = subprocess.check_output("netstat", shell=True, encoding='utf-8').strip()
	hostname: str = subprocess.check_output("hostname", shell=True, encoding='utf-8').strip()
	active_tcp: str = subprocess.check_output("netstat -atnp", shell=True, encoding='utf-8').strip()
	active_udp: str = subprocess.check_output("netstat -aunpp", shell=True, encoding='utf-8').strip()
	interfaces: str = subprocess.check_output("ip -brief address", shell=True, encoding='utf-8').strip()
	listening_ports: str = subprocess.check_output("netstat -ltnp", shell=True, encoding='utf-8').strip()
	firewall_rules: str = subprocess.check_output("ufw status", shell=True, encoding='utf-8').strip()

	print("\nNetwork Statistics:")
	print(f"  Hostname               - {hostname}")
	print(f"  Active TCP connections - \n{active_tcp}")
	print(f"  Active UDP connections - \n{active_udp}")
	print(f"  Whole netstat output   - \n{basic_netstat}")
	print(f"  Interfaces             - \n{interfaces}")
	print(f"  Listening ports        - \n{listening_ports}")
	print(f"  Firewall rules         - \n{firewall_rules}")

	try:
		socket.setdefaulttimeout(1)
        ping_target_url: str = "www.gnu.org"
		host: str = socket.gethostbyname()
		internet_connection = socket.create_connection((host, 80), 2)
		internet_connection.close()

		print(f"\nSuccessfully pinged {ping_target_url}: System is online.")
	except OSError:
		print("\nNetwork is unreachable. System is not connected to the Internet.")

	try:
		api_url: str = "https://api.ipify.org"
		response = requests.get(api_url)
		print(f"System's IP-Address: {response.text}")
	except OSError:
		print("\nCould not resolve the system's IP-Address.")
