#!/usr/bin/python3

"""
---------------------------------------
Manages your OpenSSH. It can:
- Hardens your SSH by configuring the sshd_config file. Essential to your server!
- Logs SSH connections to your server
GNU/Linux and BSD supported.

Author: iva,
        zaw (ssh_logging)
Date: 03.07.2024
---------------------------------------
"""

try:
    import re
    import usr
    import subprocess
    from os import system
    from time import sleep
    from usr import RED, GREEN, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")
    exit(1)


def ssh_logging() -> None:
    system("clear")

    print("We are going to log SSH connections to your device.")
    if usr.prompt_user("[?] Proceed?"):
        log_file_path: str = input("[==>] Enter log file path [default]:")
        if log_file_path == "":
            log_file_path: str = "/var/log/auth.log" or "/var/log/secure"

        with open(log_file_path, "r") as log_file:
            log_file.seek(0, 2)
            loading: int = 0

            while True:
                try:
                    line: str = log_file.readline()
                    if not line:
                        print("+-------- No new log entries --------+")
                        print("." * (loading % 3 + 1), end="\r")
                        loading += 1
                        sleep(5)
                        continue
                    else:
                        loading: int = 0

                    if re.search(r"Accepted.*from", line):
                        print("+-------- SSH connection detected --------+")
                        print({line.strip()})
                except KeyboardInterrupt:
                    break


def safe_ssh_setup() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()

    print("[*] After running this module, the following changes will be made:")
    print("0. Install openssh-client and openssh-server.")
    print("1. Remove password authentication.")
    print("2. Add Pubkey authentication.")
    print("3. Permit root login.")
    print("4. Set MaxAuthTries to 3.")
    print("5. Change port value from 22 to 1984.")
    print("*. Many more.")

    if usr.prompt_user("[?] Proceed?"):
        if usr.is_debian_based(distro):
            usr.package_handling(distro, package_list=["openssh-client", "openssh-server"], command="install")
        elif distro in usr.FREEBSD_BASED_DISTROS or distro in usr.OPENBSD_BASED_DISTROS or distro in usr.NETBSD_BASED_DISTROS:
            print("[*] Assuming you already have openssh (BSD).")
        else:
            usr.package_handling(distro, package_list=["openssh"], command="install")
    
        try:
            with open("config_files/secure_ssh_config.txt", "r") as config_file:
                secure_ssh_config_text: str = config_file.read()

            with open("/etc/ssh/sshd_config", "w") as true_config_file:
                true_config_file.write(secure_ssh_config_text)
        
            if init_system == "systemd":
                usr.init_system_handling("systemd", "start", "sshd")
            else:
                usr.init_system_handling(init_system, "start", "ssh")

            print(f"{GREEN}[*] Success! {RESET}")
        except (FileNotFoundError, IOError):
            print(f"{RED}[!] Configuration file 'config_files/secure_ssh_config.txt' not found.\nBroken installation?{RESET}")


def ssh_management() -> None:
    system("clear")

    functions: dict = {
        "safe_ssh_setup": safe_ssh_setup,
        "ssh_logging": ssh_logging
    }

    print("+---- SSH Management  ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__":
    ssh_management()
    
