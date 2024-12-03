#!/usr/bin/python3

"""
---------------------------------------
Setups tor functionality on your machine.

- Installs tor on your machine
- Setups tor nodes.
- Adds Tor repositories for Devuan and Debian GNU/Linux.

Author: iva
Date: 02.12.2024
---------------------------------------
"""

try:
    import usr
    import subprocess
    from os import system
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as error:
    print(f"{RED}[!] Error: modules not found:\n{error}{RESET}")


def tor_node_setup() -> None:
    system("clear")
    ...


def install_tor() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    print("We are going to install tor on your machine.")

    answer: str = input("\n[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=["tor", "torsocks"], command="install")
            
            print("Now you need to install Tor Browser from the web.")
            answer: str = input("[?] Proceed? (y/N): ")
            if answer in ["y", "yes"]:
                subprocess.run(["xdg-open", "https://www.torproject.org/download/"], check=True)
            
            print("Looks like you're locked and loaded.")
            print("Tor can't help you if you use it wrong! Learn how to be safe at https://support.torproject.org/faq/staying-anonymous/")
            answer: str = input("[?] Proceed? (y/N): ")
            if answer in ["y", "yes"]:
                subprocess.run(["xdg-open", "https://support.torproject.org/faq/staying-anonymous/"], check=True)
            
            print(f"{GREEN}[*] Success! {RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def snowflake_setup_debian() -> None:
    system("clear")
    ...


def snowflake_setup_freebsd() -> None:
    system("clear")
    ...


def torify_apt_devuan() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro != "devuan":
        print(f"{RED}[!] Error: your OS {distro} is not devuan based.{RESET}")

    print("Tor is a free overlay network for enabling anonymous communication.")
    print("Built on free and open-source software and more than seven thousand volunteer-operated relays worldwide,") 
    print("users can have their Internet traffic routed via a random path through the network.")
    print("And if you wish, you can use apt over tor (Devuan based GNU/Linux distribution required).")

    answer: str = input("\n[?] Proceed? (y/N): ").lower()
    if answer in ["y", "yes"]:
        try:
            usr.package_handling(distro, package_list=["tor", "apt-transport-tor"], command="install")
            
            print("[?] Start tor service now? (y/N): ")
            if answer in ["y", "yes"]:
                usr.init_system_handling(init_system, "start", "tor")
            
            with open("config_files/apt_tor_devuan_repos.txt", "r") as config_file:
                apt_tor_repos: str = config_file.read()

            with open("/etc/apt/sources.list", "a") as true_config_file:
                true_config_file.write(apt_tor_repos)
            
            print(f"{GREEN}[*] Success!{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def torify_apt_debian() -> None:
    system("clear")
    ...


def tor_management() -> None:
    system("clear")

    functions: dict = {
            "install_tor": install_tor,
            "torify_apt_debian": torify_apt_debian,
            "torify_apt_devuan": torify_apt_devuan,
            "snowflake_setup_debian": snowflake_setup_debian,
            "snowflake_setup_freebsd": snowflake_setup_freebsd,
            "tor_node_setup": tor_node_setup
            }

    print("+---- Tor Management  ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__": 
    tor_management()
