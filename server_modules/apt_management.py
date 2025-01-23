#!/usr/bin/python3

"""
---------------------------------------
Tweaks for Apt Package Manager.
- Adds 32-bit libraries.
- Reduces the risk of vulnerabilities being exploited and helps keep your system stable and secure.
- Adds Debian 12 Bookworm Backports
Debian-Based GNU/Linux distributions only supported.

Author: iva
Date: 28.07.2024
---------------------------------------
"""

try:
    import subprocess
    import the_unix_manager as tum
    from the_unix_manager import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found.\n{import_error}.{RESET}")


def enable_auto_updates() -> None:
    """
    Enables autoupdates on Debian based systems via unattended-upgrades package.
    """

    print("\nAutomatic updates help ensure your system is always protected with the latest security patches and improvements.")
    print("By enabling automatic updates, your system will regularly check for updates and install them without manual intervention.")
    print("This reduces the risk of vulnerabilities being exploited and helps keep your system stable and secure.")

    if tum.prompt_user("[?] Proceed?"):
        print(f"[<==] Enabling automatic updates...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "unattended-upgrades", "-y"], check=True)
        subprocess.run(["dpkg-reconfigure", "-plow", "unattended-upgrades"], check=True)
       
        try:
            with open("/etc/tsf/module_configs/auto_update_config.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/apt/apt.conf.d/20auto-upgrades", "w") as true_config_file:
                true_config_file.write(config_file_text)

            print(f"\n{GREEN}[*] Automatic updates have been enabled.{RESET}")
        except (FileNotFoundError, IOError):
            print(f"{RED}[!] Error: Configuration file not found.{RESET}")


def disable_auto_updates() -> None:
    """
    Disable autoupdates on Debian based systems.
    """

    print("Disabling automatic updates will stop your system from automatically checking for and installing updates.")
    print("This may leave your system vulnerable to unpatched security issues.")

    if tum.prompt_user("[?] Proceed?"):
        print("[<==] Disabling automatic updates...")
        try:
            with open("/etc/tsf/module_configs/disable_auto_update_config.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/apt/apt.conf.d/20auto-upgrades", "w") as true_config_file:
                true_config_file.write(config_file_text)

            print(f"\n{GREEN}[*] Automatic updates have been disabled.{RESET}")
        except (FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: Configuration files not found:\n{error}{RESET}")


def enable_debian_backports() -> None:
    """

    """

    print("Backports are packages taken from the next Debian release (called 'testing'), adjusted and recompiled for usage on Debian stable.")
    print("By adding Debian Backports, you can gradually increase the number of fresh/completely new packages on your system.")

    if tum.prompt_user("[?] Enable Backports?"):
        print("[<==] Enabling Backports...")
        try:
            with open("/etc/tsf/module_configs/apt_debian_backports.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/apt/sources.list", "a") as true_config_file:
                true_config_file.write(config_file_text)
            
            if tum.prompt_user("[?] Check 'sources.list'?"):
                subprocess.run(["nano", "/etc/apt/sources.list"], check=True)

            print(f"\n{GREEN}[*] Backports are successfully added.{RESET}")
        except (FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: Configuration files not found:\n{error}{RESET}")


def add_i386() -> None:
    """

    """

    print("Some specific software requires 32-bit libraries to work.")
    if tum.prompt_user("[?] Add i386 support?"):
        print("[<==] Adding architecture...")
        try:
            subprocess.run(["dpkg", "--add-architecture", "i386"], check=True)
            tum.package_handling("debian", package_list=[], command="update")
            print(f"{GREEN}[*] Success!{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError) as dpkg_error:
            print(f"{RED}[!] Error: {dpkg_error}{RESET}")


def apt_management() -> None:
    """
    Main function.
    """

    distro: str = tum.get_user_distro()
    debian: bool = tum.is_debian_based(distro)
    if not debian:
        print(f"{RED}[!] Error: Your OS {distro} is not Debian based.{RESET}")

    functions: dict = {
            "enable_auto_updates": enable_auto_updates,
            "disable_auto_updates": disable_auto_updates,
            "enable_debian_backports": enable_debian_backports,
            "add_i386": add_i386
            }

    print("+---- Auto Updates  ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__":
    apt_management()
