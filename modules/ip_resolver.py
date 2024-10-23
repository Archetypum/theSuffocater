#!/usr/bin/python3

"""
---------------------------------------
Resolves Country, city and company of provided IP address.

GNU/Linux, BSD, OS X and Windows supported.
Author: iva
Date: 16.08.2024
---------------------------------------
"""

import os
import json
import urllib.request as urllib2


def get_ip_details(ip_address: str) -> str | None:
    try:
        url: str = "http://ip-api.com/json/"
        response = urllib2.urlopen(url + ip_address)
        data = response.read()
        values = json.loads(data)
        print(values)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def ip_resolver() -> None:
    print("\nWe are going to resolve IP-Address country, city and company.")
    answer: str = input("\nAre you sure you want this? (y/n): ")
    if answer in ["y", "yes"]:
        ip_address: str = input("Enter IP address: ")
        get_ip_details(ip_address)
