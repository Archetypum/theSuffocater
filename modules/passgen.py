#!/usr/bin/python3

"""
---------------------------------------
Simple password generator that uses random symbols + random word from the dictionary.
Linux, BSD, Windows, OS X supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

import string
import secrets


def passgen() -> None:
    print("\nWe are going to create a strong password.")

    answer: str = input("\n[*] Are you sure you want this? (y/n): ").lower()
    if answer in ["y", "yes"]:
        name: str = input("\n[*] Enter password name: ")
        password_length: int = int(input("[*] Enter password length: "))
        
        characters: str = string.ascii_letters + string.digits
        with open("config_files/passgen_dict.txt", "r") as words_dict:
            word_list: list = [word.strip().strip("'") for word in words_dict.read().split(",")]

        created_password: str = "".join(secrets.choice(characters) for _ in range(password_length)) + secrets.choice(word_list)

        with open(f":{name}.txt", "w") as password_file:
            password_file.write(f"{name} {created_password}")

        print(f"[*] Your new password for {name}: {created_password}")
        print(f"[*] Saving to {name}.txt...")
