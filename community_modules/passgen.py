#!/usr/bin/python3

"""
---------------------------------------
Simple password generator that uses random symbols + random word from the dictionary.
GNU/Linux, BSD, Windows, OS X supported.

Author: iva,
        WretchOfLights (calculate_crack_time, crack_time)
Date: 28.07.2024
---------------------------------------
"""

try:
    import math
    from sys import exit
    from secrets import choice
    import the_unix_manager as tum
    from string import ascii_letters, digits
    from the_unix_manager import GREEN, RED, RESET

    characters: str = ascii_letters + digits
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: Modules not found. Broken installation?\n\n{import_error}{RESET}")
    exit(1)


def generate_password(password_length: int = None, word_list: list = None, characters: str = None) -> str:
    """
    Generates random password consisting of random characters and a word from 'word_list'.

    Args:
        password_length (int): Password length.
        word_list (list): Word list from /etc/tsf/module_configs/passgen_dict.txt
        characters (str): Random characters.

    Returns:
        str: Generated password.
    """

    if None in (password_length, word_list, characters):
        print(f"{RED}[!] Error: No arguments specified.\nPlease launch this function from 'passgen' directly.{RESET}")
    else:
        return "".join(choice(characters) for _ in range(password_length)) + choice(word_list)


def calculate_crack_time(password: str = None, characters: str = None) -> str:
    """
    Estimates the time it would take to crack a password using a brute-force attack.

    Args:
        password (str): Password.
        characters (str): Characters used in password.

    Returns:
        str: Estimated cracking time.
    """
    
    password_length: int = len(password)
    character_set_size: int = len(characters) 
    attempts_per_second: int = 10_000_000_000
    total_combinations: float = float(math.pow(character_set_size, password_length))
    seconds: float = total_combinations / attempts_per_second
    
    if seconds < 1:
        return "Less than a second"
    elif seconds < 60:
        return f"{round(seconds, 2)} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{round(minutes, 2)} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{round(hours, 2)} hours"
    elif seconds < 31536000:
        days = seconds / 86400
        return f"{round(days, 2)} days"
    elif seconds < 31536000 * 100:
        years = seconds / 31536000
        return f"{round(years, 2)} years"
    else:
        centuries = seconds / (31536000 * 100)
        return f"{round(centuries, 2)} centuries"


def password_generator() -> None:
    """
    Handles password generation.
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

        password_options: list = [generate_password(password_length, word_list, characters) for _ in range(3)]

        print("\n[==>] Password options:")
        for idx, password in enumerate(password_options, 1):
            print(f"    [{idx}] {password}")

        while True:
            password_choice: str = input("\n[==>] Password to save (1/2/3) or 'r' to re-roll: ").strip().lower()
            if choice in ["r", "re", "reload"]:
                print("[<==] Re-rolling the passwords...\n")
                password_options: list = [generate_password(password_length, word_list, characters) for _ in range(3)]
                print("\n[==>] Here are three new generated password options:")
                for idx, password in enumerate(password_options, 1):
                    print(f"[{idx}] {password}")
            elif choice in ["1", "2", "3"]:
                chosen_password: str = password_options[int(password_choice) - 1]
                with open(f"{name}.txt", "w") as password_file:
                    password_file.write(f"{name} {chosen_password}")
                print(f"\n[*] Your new password for {name}: {chosen_password}")
                print(f"[<==] Saving to {name}.txt...")
                break
            else:
                print(f"{RED}[!] Error: Invalid choice.{RESET}")


def crack_time() -> None:
    """
    Handles password cracking time calculation.
    """

    print("\nWe are going to estimate time of cracking your password using a brute-force attack.")
    if tum.prompt_user("[?] Proceed?"):
        password: str = input("\n[==>] Enter your password: ")

        crack_time: str = calculate_crack_time(password, characters)
        print(f"[<==] It would take {crack_time} to crack your password.")


def passgen() -> None:
    """
    Main function.
    """
       
    tum.clear_screen()

    functions: dict = {
        "password_generator": password_generator,
        "crack_time": crack_time
    }

    print("+---- Passgen ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__":
    passgen()
