#!/usr/bin/python3

"""
---------------------------------------
Pre-build fail2ban configurations.
Saves your server from bruteforce and DDoS attacks.

GNU/Linux supported.
Author: iva
Date: 23.12.2024
---------------------------------------
"""

try:
    import os
    import usr
    import subprocess
    from sys import exit
    from os import system
    from time import sleep
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def reload_fail2ban() -> bool:
    init_system: str = usr.get_init_system()

    usr.init_system_handling(init_system, "reload", "fail2ban")
    usr.init_system_handling(init_system, "start", "fail2ban")	

	
def create_jail_copy() -> None:
    system("clear")

    print("We are going to create a copy of 'jail.conf' with name 'jail.local'.")
    if usr.prompt_user("[?] Proceed?"):
        try:
            print("[<==] Creating a copy of 'jail.conf' file...")
            sleep(1)
            if not os.path.exists("/etc/fail2ban/jail.local"):
                subprocess.run(["cp", "/etc/fail2ban/jail.conf", "/etc/fail2ban/jail.local"], check=True)
            else:
                print(f"{GREEN}[*] 'jail.local' is already exists.")
            print(f"[*] Success!{RESET}")
        except (IOError, FileNotFoundError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def ssh_bruteforce() -> None:
    system("clear")
    
    init_system: str = usr.get_init_system()

    print("We are going to configure fail2ban to prevent SSH bruteforce.")
    if usr.prompt_user("[?] Proceed?"):
        try:
            with open("config_files/fail2ban_ssh_bruteforce.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/fail2ban/jail.local", "a") as true_config_file:
                true_config_file.write(config_file_text)

            input("[==>] Hit enter to check /etc/fail2ban/jail.local ...")
            subprocess.run(["nano", "/etc/fail2ban/jail.local"], check=True)
            
            if init_system == "systemd":
                usr.init_system_handling("systemd", "enable", "sshd")
                usr.init_system_handling("systemd", "reload", "ssh")
                usr.init_system_handling("systemd", "start", "ssh")
            else:
                usr.init_system_handling(init_system, "reload", "ssh")
                usr.init_system_handling(init_system, "start", "ssh")
            reload_fail2ban()
            
            print(f"{GREEN}[*] Success!{RESET}")
            sleep(3)
            fail2ban_setup()
        except (IOError, FileNotFoundError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def ftp_bruteforce() -> None:
    system("clear")

    init_system: str = usr.get_init_system
    print("We are going to configure fail2ban to prevent FTP bruteforce.")
    if usr.prompt_user("[?] Proceed?"):
        try:
            with open("config_files/fail2ban_ftp_bruteforce.txt") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/fail2ban/jail.local", "a") as true_config_file:
                true_config_file.write(config_file_text)
            
            input("[==>] Hit enter to check /etc/fail2ban/jail.local ...")
            subprocess.run(["nano", "/etc/fail2ban/jail.local"], check=True)
            reload_fail2ban()
            
            print(f"{GREEN}[*] Success!{RESET}")
            sleep(3)
            fail2ban_setup()
        except (IOError, FileNotFoundError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def fail2ban_setup() -> None:
    system("clear")

    profiles: dict = {
            "create_jail_copy": create_jail_copy,
            "ssh_bruteforce": ssh_bruteforce,
            "ftp_bruteforce": ftp_bruteforce
            }
    
    print("+---- Fail2Ban Setup ----+")
    print("\nAvailable functions:")
    for profile in profiles.keys():
        print(f" - {profile}")
    
    while True:
        try:
            your_profile: str = input("[==>] Enter profile: ").lower()
            if your_profile in profiles:
                profiles[your_profile]()
            else:
                print(f"{RED}[!] Error: {your_profile} is not defined.{RESET}")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    fail2ban_setup()
