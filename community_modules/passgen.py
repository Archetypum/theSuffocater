#!/usr/bin/python3

"""
---------------------------------------
Simple password generator that uses random symbols + random word from the dictionary.
GNU/Linux, BSD, Windows, OS X supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

try:
    import math
    from sys import exit
    from secrets import choice
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
    from string import ascii_letters, digits, punctuation
    
    characters: str = ascii_letters + digits + punctuation
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: Modules not found. Broken installation?\n\n{import_error}{RESET}")
    exit(1)


def generate_password(password_length: int = None, word_list: list = None) -> str:
    """
    Generates random password consisting of random characters and a word from 'word_list'.

    Args:
        password_length (int): Password length.
        word_list (list): Word list from /etc/tsf/module_configs/passgen_dict.txt

    Returns:
        str: Generated password.
    """

    if None in (password_length, word_list, characters):
        print(f"{RED}[!] Error: No arguments specified.\nPlease launch this function from 'passgen' directly.{RESET}")
    else:
        return "".join(choice(characters) for _ in range(password_length)) + choice(word_list)


def passgen() -> None:
    """
    [*] MAIN FUNCTION [*]
    """

    print("\nWe are going to create a strong password.")
    if tum.prompt_user("[?] Proceed?"):
        name: str = input("\n[==>] Enter password name: ")

        while True:
            try:
                password_length: int = int(input("[==>] Enter password length: "))
                break
            except ValueError:
                print(f"{RED}[!] Error: Invalid password length. Please enter a number.{RESET}")

        with open("/etc/tsf/module_configs/passgen_dict.txt", "r") as words_dict:
            word_list: list = [word.strip().strip("'") for word in words_dict.read().split(",")]

        password_options: list = [generate_password(password_length, word_list) for _ in range(3)]

        print("\n[==>] Password options:")
        for idx, password in enumerate(password_options, 1):
            print(f"    [{idx}] {password}")

        while True:
            password_choice: str = input("\n[==>] Password to save (1/2/3) or 'r' to re-roll: ").strip().lower()
            if password_choice in ["r", "re", "reload"]:
                print("[<==] Re-rolling the passwords...\n")
                password_options: list = [generate_password(password_length, word_list) for _ in range(3)]
                print("\n[==>] Here are three new generated password options:")
                for idx, password in enumerate(password_options, 1):
                    print(f"[{idx}] {password}")
            elif password_choice in ["1", "2", "3"]:
                chosen_password: str = password_options[int(password_choice) - 1]
                with open(f"{name}.txt", "w") as password_file:
                    password_file.write(f"{name} {chosen_password}")
                print(f"\n[*] Your new password for {name}: {chosen_password}")
                print(f"[<==] Saving to {name}.txt...")
                break
            else:
                print(f"{RED}[!] Error: Invalid choice.{RESET}")


if __name__ == "__main__":
    passgen()
