#!/usr/bin/python3

"""
---------------------------------------
Resolves Country, city and company of provided IP address.

GNU/Linux, BSD, OS X and Windows supported.
Author: iva
Date: 16.08.2024
---------------------------------------
"""

try:
    import os
    import usr
    import json
    import urllib.request as urllib2
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")


def get_ip_details(ip_address: str) -> None:
    url: str = "http://ip-api.com/json/"
    response = urllib2.urlopen(url + ip_address)
    data = response.read()
    values = json.loads(data)
    if values.get("status") == "fail":
        print(f"{RED}[!] Error: Could not resolve IP address {ip_address}{RESET}")
        return
    
    print(f"{GREEN}{values}{RESET}")


def ip_resolver() -> None:
    ip_address: str = input("[==>] Enter IP address: ")
    if usr.is_valid_ip(ip_address):
        get_ip_details(ip_address)
    else:
        print(f"{RED}[!] Error: IP is not valid.{RESET}")


if __name__ == "__main__":
    ip_resolver()
