#!/usr/bin/python3

"""
---------------------------------------
Manages your OpenSSH. It can:
- Hardens your SSH by configuring the sshd_config file. Essential to your server!
- Logs SSH connections to your server
GNU/Linux and BSD supported.

Authors: iva,
         zaw (ssh_logging, ssh_key_gen)
Date: 03.07.2024
---------------------------------------
"""

try:
    import os
    import re
    import usr
    import subprocess
    from os import system
    from time import sleep
    from usr import RED, GREEN, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")
    exit(1)


def ssh_key_gen() -> None:
    system("clear")
        
    key_type: str = input("[==>] Select key type (rsa, dsa, ecdsa, ed25519; enter for default - rsa): ")
    key_size: str = input("Select key size (1024, 2048, 3072 for rsa/dsa; enter for default - 2048): ")
    
    if key_type == "":
        key_type = "rsa"
        
    if key_size == "":
        key_size = "2048"

    valid_key_types = ["rsa", "dsa", "ecdsa", "ed25519"]
    valid_key_sizes = {
        "rsa": ["1024", "2048", "3072", "4096"],
        "dsa": ["1024", "2048", "3072"],
        "ecdsa": ["256", "384", "521"],
        "ed25519": ["256"],
    }

    if key_type not in valid_key_types:
        print(f"{RED}[!] Error: Invalid key type: {key_type}{RESET}")
        print("Available types: rsa, dsa, ecdsa, ed25519.")
        return
    
    if key_size not in valid_key_sizes.get(key_type, []):
        print(f"{RED}[!] Error: Size {key_size} is not valid for key type {key_type}{RESET}")
        print(f"Available key sizes for {key_type}: {', '.join(valid_key_sizes.get(key_type, []))}.")
        return 
    
    key_name = f"~/.ssh/id_{key_type}"
    key_file = os.path.expanduser(key_name)

    command = ["ssh-keygen", "-t", key_type]
    if key_type != "ed25519":
        command += ["-b", key_size]
    command += ["-f", key_file, "-N", ""]

    try:
        subprocess.run(command, check=True)
        print(f"Your SSH-keys: {key_file} и {key_file}.pub")
    except subprocess.CalledProcessError:
        print("{RED}[!] Error: failed to create SSH-keys: {error}")
        return


def ssh_logging() -> None:
    system("clear")

    print("We are going to log SSH connections to your device.")
    if usr.prompt_user("[?] Proceed?"):
        log_file_path: str = input("[==>] Enter log file path [default]: ")
        
        if log_file_path == "":
            if os.path.exists("/var/log/auth.log"):
                log_file_path: str = "/var/log/auth.log"
            elif os.path.exists("/var/log/secure"):
                log_file_path: str = "/var/log/secure"
            else:
                print(f"{RED}[!] Error: Log file not found. Creating a new one...")
                try:
                    subprocess.run(["touch", "/var/log/auth.log"], check=True)
                    log_file_path: str = "/var/log/auth.log"
                except subprocess.CalledProcessError as error:
                    print(f"{RED}[!] Error: Failed to create log file: {error}")
                    return

        try:
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
                            print(line.strip())
                    except KeyboardInterrupt:
                        break
        except FileNotFoundError:
            print(f"{RED}[!] Error: Log file {log_file_path} does not exist.")


def safe_ssh_setup() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()

    print("After running this module, the following changes will be made:")
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
        "ssh_logging": ssh_logging,
        "key_management": key_management,
        "ssh_key_gen": ssh_key_gen     
    }

    print("+---- SSH Management  ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__":
    ssh_management()
    
