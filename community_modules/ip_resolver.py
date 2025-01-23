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
    import re
    import json
    import urllib
    import the_unix_manager as tum
    import urllib.request as urllib2
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def is_valid_ip(ip_address: str = None) -> bool:
    """
    Args:
        ip_address (str): target IP address.
    
    Returns:
        bool: If provided IP is valid
    """
    
    if ip_address is None:
        ip_address: str = input("\n[==>] Enter target IP address: ")

    pattern: str = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip_address) is not None


def get_ip_details(ip_address: str = None) -> None:
    """
    Gets ip details.

    Args:
        ip_address (str): Target IP address. 

    Returns:
        None: Nothing.
    """

    if ip_address is None:
        ip_address: str = input("\n[==>] Enter target IP address: ")

    try:
        url: str = "http://ip-api.com/json/"
        response = urllib2.urlopen(url + ip_address)
        data: str = response.read()
        values = json.loads(data)
        if values.get("status") == "fail":
            print(f"{RED}[!] Error: Could not resolve IP address {ip_address}{RESET}")
            return
    
        print(f"{GREEN}{values}{RESET}")
    except urllib.error.URLError:
        print(f"{RED}[!] Error: No Internet connection.{RESET}")


def ip_resolver() -> None:
    """
    Main function.
    """

    ip_address: str = input("[==>] Enter target IP address: ")
    if is_valid_ip(ip_address):
        get_ip_details(ip_address)
    else:
        print(f"{RED}[!] Error: IP is not valid.{RESET}")


if __name__ == "__main__":
    ip_resolver()
