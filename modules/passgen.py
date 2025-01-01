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
    import usr
    import string
    import secrets
    from sys import exit
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")
    exit(1)


def passgen() -> None:
    print("\nWe are going to create a strong password.")
    if usr.prompt_user("[?] Proceed?"):
        try:
            name: str = input("\n[==>] Enter password name: ")
            password_length: int = int(input("[==>] Enter password length: ")) 

            characters: str = string.ascii_letters + string.digits
            with open("config_files/passgen_dict.txt", "r") as words_dict:
                word_list: list = [word.strip().strip("'") for word in words_dict.read().split(",")]

            created_password: str = "".join(secrets.choice(characters) for _ in range(password_length)) + secrets.choice(word_list)
            with open(f"{name}.txt", "w") as password_file:
                password_file.write(f"{name} {created_password}")

            print(f"[*] Your new password for {name}: {created_password}")
            print(f"[<==] Saving to {name}.txt...")
        except ValueError:
            print(f"{RED}[!] Error: password length cant be {password_length}{RESET}")


if __name__ == "__main__":
    passgen()
