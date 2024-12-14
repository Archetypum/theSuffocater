#!/usr/bin/python3

"""
---------------------------------------
Disables Geoclue geolocation gathering, improving your OPSEC.

Author: iva
Date: 02.12.2024
---------------------------------------
"""

try:
    import usr
    from os import system
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")


def safe_geoclue_setup() -> None:
    system("clear")

    print("This script is going to set all geoclue config variables to 'false'.")
    print("Your GNOME/KDE desktop system will stop using your geolocation.")

    if usr.prompt_user("[?] Proceed?"):
        try:
            with open("config_files/safe_geoclue_config.txt", "r") as config_file:
                geoclue_config_text: str = config_file.read()

            with open("/etc/geoclue/geoclue.conf", "w") as true_config_file:
                true_config_file.write(geoclue_config_text)

            print(f"{GREEN}[*] Geoclue is successfully disabled.{RESET}")
        except (FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


if __name__ == "__main__":
    safe_geoclue_setup()
