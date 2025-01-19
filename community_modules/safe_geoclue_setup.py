#!/usr/bin/python3

"""
---------------------------------------
Disables Geoclue geolocation gathering, improving your OPSEC.

Author: iva
Date: 02.12.2024
---------------------------------------
"""

try:
    import os
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def safe_geoclue_setup() -> None:
    tum.clear_screen()

    print("This script is going to set all geoclue config variables to 'false'.")
    print("Your system will stop using your geolocation.")

    if tum.prompt_user("[?] Proceed?"):
        try:
            with open("/etc/tsf/module_configs/safe_geoclue_config.txt", "r") as config_file:
                geoclue_config_text: str = config_file.read()

            with open("/etc/geoclue/geoclue.conf", "w") as true_config_file:
                true_config_file.write(geoclue_config_text)

            print(f"{GREEN}[*] Geoclue is successfully disabled.{RESET}")
        except (FileNotFoundError, IOError) as file_error:
            if not os.path.exists("/etc/geoclue/geoclue.conf"):
                print(f"{GREEN}[*] '/etc/geoclue/geoclue.conf' not found. What a relief!")
                print(f"[*] Success!{RESET}")
            else:
                print(f"{RED}[!] Error: {file_error}{RESET}")
            

if __name__ == "__main__":
    safe_geoclue_setup()
