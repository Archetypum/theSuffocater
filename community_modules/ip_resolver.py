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
    import json
    from re import match
    import the_unix_manager as tum
    import urllib.request as urllib2
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def is_valid_ip(ip_address: str) -> bool:
    """
    Args:
        ip (str): target IP address.
    
    Returns:
        bool: If provided IP is valid
    """

    pattern: str = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return match(pattern, ip_address) is not None


def get_ip_details(ip_address: str) -> None:
    """
    Gets ip details.

    Args:
        ip_address (str): Target IP address.

    Returns:
        None: Nothing.
    """

    url: str = "http://ip-api.com/json/"
    response = urllib2.urlopen(url + ip_address)
    data: str = response.read()
    values = json.loads(data)
    if values.get("status") == "fail":
        print(f"{RED}[!] Error: Could not resolve IP address {ip_address}{RESET}")
        return
    
    print(f"{GREEN}{values}{RESET}")


def ip_resolver() -> None:
    """
    Main function
    """

    ip_address: str = input("[==>] Enter IP address: ")
    if is_valid_ip(ip_address):
        get_ip_details(ip_address)
    else:
        print(f"{RED}[!] Error: IP is not valid.{RESET}")


if __name__ == "__main__":
    ip_resolver()
