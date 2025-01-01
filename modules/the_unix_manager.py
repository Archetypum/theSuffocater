#!/usr/bin/python3

"""
---------------------------------------
This is theUnixManager - ultimate package manager && init system handler
made by Archetypum that simplifies interaction with UNIX systems and creation of system-related python scripts.

Archetypum: (https://github.com/Archetypum)
Github repo link: (https://github.com/Archetypum/theUnixManager)
Real usage example: (https://github.com/Archetypum/theSuffocater)

TODO:
    * add logging functionality arguments.
    * test this on more systems.
    * add bash version.
    * many more?

Date: 18.10.2024
---------------------------------------
"""

# theUnixManger version:
the_unix_manager_version: str = "v1.0.0-unstable"

# ANSI Color codes and text formating:
BLACK: str = "\033[90m"
WHITE: str = "\033[97m"
YELLOW: str = "\033[93m"
ORANGE: str = "\033[38;5;214m"
BLUE: str = "\033[94m"
PURPLE: str = "\033[95m"
GREEN: str = "\033[92m"
RED: str = "\033[91m"
BOLD: str = "\033[1m"
UNDERLINE: str = "\033[4m"
REVERSED: str = "\033[7m"
ITALIC: str = "\033[3m"
CROSSED_OUT: str = "\033[9m"
RESET: str = "\033[0m"

# GNU/Linux operating systems:
DEBIAN_BASED: list = ["debian", "ubuntu", "xubuntu", "linuxmint", "lmde", "trisquel", "devuan",
                      "kali", "parrot", "pop", "elementary", "mx", "antix", "crunchbag",
                      "crunchbag++", "pureos", "deepin", "zorin", "peppermintos", "lubuntu",
                      "kubuntu", "wubuntu", "steamos", "astra", "tails", "ututos", "ulteo",
                      "aptosid", "canaima", "corel", "dreamlinux", "elive", "finnix",
                      "gibraltar", "gnulinex", "kanotix", "kurumin", "linspire", "maemo",
                      "mepis", "vyatta", "solusos", "openzaurus", "cutefishos"]
ARCH_BASED: list = ["arch", "artix", "manjaro", "endeavouros", "garuda", "parabola", "hyperbola",
                    "archbang", "blackarch", "librewolf", "chakra", "archex", "archman", "arco",
                    "bluestar", "chimeraos", "instantos", "kaos", "rebornos", "archhurd", "cyberos"]
ALPINE_BASED: list = ["alpine", "postmarket"]
GENTOO_BASED: list = ["gentoo", "pentoo", "funtoo", "calculate" "chromeos", "vidalinux", "knopperdisk"
                      "gentoox", "sabayon", "chromiumos", "tinhatlinux", "ututo"]
VOID_BASED: list = ["void", "argon", "shikake", "pristine"]
DRAGORA_BASED: list = ["dragora"]
SLACKWARE_BASED: list = ["slackware", "salixos", "simplelinux", "basiclinux", "frugalware", "austrumi",
                         "hostgis", "kateos", "mulinux", "nimblex", "platypux", "slackintosh", "slax",
                         "supergamer", "topologilinux", "vectorlinux", "wolvix", "zenwalk", "zipslack"]
FEDORA_BASED: list = ["fedora", "mos"]
CENTOS_BASED: list = ["centos"]
GUIX_BASED: list = ["guix"]

# BSD UNIX operating systems:
FREEBSD_BASED: list = ["freebsd", "midnightbsd", "ghostbsd", "bastillebsd", "cheribsd", "dragonflybsd",
                       "trueos", "hardenedbsd", "hellosystem", "truenas", "nomadbsd", "clones", "junosos",
                       "xigmanas", "opnsense", "pfsense", "cellos", "orbisos", "zrouter", "ulbsd", "ravynos"]
OPENBSD_BASED: list = ["openbsd", "adj", "libertybsd", "bitrig", "bowlfish", "ekkobsd", "embsd", "fabbsd",
                       "fuguita", "marbsd", "microbsd", "miros", "olivebsd", "psygnat", "quetzal",
                       "sonafr"]
NETBSD_BASED: list = ["netbsd", "blackbsd", "edgebsd", "seos", "os108", "jibbed"]

try:
    import os
    import re
    import platform
    import subprocess
    from sys import exit
    from time import sleep
    from typing import List
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: python modules not found. Broken installation?:\n{import_error}{RESET}")


def the_unix_manager_version() -> str:
    """
    Returns:
         str: theUnixManager version.
    """

    return the_unix_manager_version

def the_unix_manager_tester() -> None:
    """
    Small autotests.

    Returns:
         None: nothing.
    """
    successfully_tested: list = []
    init_system: str = get_init_system()
    distro: str = get_user_distro()

    print(f"user distro: {distro}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"user init system: {init_system}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{BLACK}black text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{YELLOW}yellow text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{ORANGE}orange text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{BLUE}blue text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{PURPLE}purple text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{GREEN}green text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{RED}red text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{BOLD}bold text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{UNDERLINE}underlined text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{REVERSED}reversed text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{ITALIC}italic text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    print(f"{CROSSED_OUT}crossed out text{RESET}")
    if prompt_user("[?] is that true?"):
        successfully_tested.append(True)

    successfully_tested.append(package_handling(distro, package_list=[], command="update"))
    successfully_tested.append(package_handling(distro, package_list=["htop"], command="remove"))
    successfully_tested.append(package_handling(distro, package_list=[], command="autoremove"))
    successfully_tested.append(init_system_handling(init_system, command="start", service="ssh"))

    if not all(successfully_tested):
        print(f"\n{ORANGE}[!] Some tests are not passed:{RESET}")
    else:
        print(f"\n{GREEN}[*] All tests are successfully passed!")
    print(successfully_tested)


# Custom theSuffocater function:
def is_valid_ip(ip: str) -> bool:
    """
    Args:
        ip (str): target IP address.
    
    Returns:
        bool: If provided IP is valid.
    """

    pattern: str = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip) is not None


# Custom theSuffocater function:
def is_valid_mac(mac: str) -> bool:
    """
    Args:
        mac (str): target MAC address.
    
    Returns:
        bool: If provided MAC is valid.
    """

    pattern: str = r"([0-9a-fA-F]{2}[:.-]){5}[0-9a-fA-F]{2}"
    return re.match(pattern, mac) is not None


def clear_screen() -> bool:
    """
    Clears user's screen.

    Returns:
        bool: cleaning status.
    """

    user_platform: str = platform.system()
    if user_platform == "Windows":
        os.system("cls")
        return True
    else:
        os.system("clear")
        return True


def is_debian_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Debian based.
    """

    return True if distro in DEBIAN_BASED else False


def is_arch_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Arch based.
    """

    return True if distro is ARCH_BASED else False


def is_alpine_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Alpine based.
    """

    return True if distro is ALPINE_BASED else False


def is_gentoo_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Gentoo based.
    """

    return True if distro is GENTOO_BASED else False


def is_void_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Void based.
    """

    return True if distro is VOID_BASED else False


def is_dragora_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Dragora based.
    """

    return True if distro is DRAGORA_BASED else False


def is_slackware_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Slackware based.
    """

    return True if distro is SLACKWARE_BASED else False


def is_fedora_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Fedora based.
    """

    return True if distro is FEDORA_BASED else False


def is_centos_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is CentOS based.
    """

    return True if distro in CENTOS_BASED else False


def is_guix_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is Guix based.
    """

    return True if distro in GUIX_BASED else False


def is_freebsd_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is FreeBSD based.
    """

    return True if distro in FREEBSD_BASED else False


def is_openbsd_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is OpenBSD based.
    """

    return True if distro in OPENBSD_BASED else False


def is_netbsd_based(distro: str) -> bool:
    """
    Returns:
        bool: If provided distro is NetBSD based.
    """

    return True if distro in NETBSD_BASED else False


def prompt_user(prompt: str, default: str = "N") -> bool:
    """
    Prompts the user for input and returns True for 'y/yes' or False for 'n/no'.
    Allows for a default value to be used if the user presses Enter without typing.

    Args:
        prompt (str): The prompt message to display to the user.
        default (str): The default value ('Y' or 'N') to assume if the user just presses Enter.

    Returns:
        bool: True for 'y', 'ye', 'yes' (case-insensitive); False for 'n', 'no' (case-insensitive).
    """

    user_input: str = input(f"{prompt} (y/N): ").strip().lower()

    if not user_input:
        user_input: str = default.lower()

    return user_input in ["y", "ye", "es", "yes"]


def get_user_distro() -> str:
    """
    Detects user GNU/Linux or BSD distribution.

    Returns:
        str: User distro name.
    """

    try:
        with open("/etc/os-release") as release_file:
            for line in release_file:
                if line.startswith("ID_LIKE="):
                    name: str = line.split("=")[1].strip().lower()
                    return name
                if line.startswith("ID="):
                    name: str = line.split("=")[1].strip().lower()
                    return name
    except FileNotFoundError:
        # BSDs don't have '/etc/os-release'.
        print(f"{RED}[!] Error: Cannot detect distribution from /etc/os-release.{RESET}")
        name: str = input("[==>] Write your OS yourself: ").strip().lower()

        return name


def get_init_system() -> str:
    """
    Detects init system.
    Can detect systemd, runit, sysvinit, openrc, s6, init, and launchd.

    Returns:
        str: Name of the init system (e.g., "systemd", "sysvinit", "upstart", "openrc", etc.)
    """

    if os.path.exists("/run/systemd/system"):
        return "systemd"

    elif os.path.exists("/etc/init.d"):
        return "sysvinit"

    elif os.path.exists("/etc/init.d") and os.path.isdir("/etc/init.d/openrc"):
        return "openrc"

    elif os.path.exists("/etc/s6"):
        return "s6"
    elif os.path.exists("/etc/runit"):
        return "runit"

    try:
        init_pid: str = subprocess.check_output(["ps", "-p", "1", "-o", "comm="]).decode().strip()
        if init_pid == "init":
            return "init"
    except subprocess.CalledProcessError:
        pass

    return "unknown"


class SystemdManagement:
    """
    A class for managing services using systemd.

    This class provides methods to perform basic operations on services,
    such as starting, stopping, reloading, and checking the status. It uses the
    'systemctl' utility to manage services and handles errors that occur during
    command execution.

    Attributes:
        command (str): The command to perform on the service (start, stop, restart, reload, status).
        service (str): The name of the service to manage.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command: str = command
        self.service: str = service

    def _run_systemctl(self, action: str) -> bool:
        try:
            subprocess.run(["systemctl", action, self.service], check=True)
            return True
        except subprocess.CalledProcessError as run_systemctl_error:
            print(f"{RED}[!] Error: {run_systemctl_error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_systemctl("start")

    def stop_service(self) -> bool:
        return self._run_systemctl("stop")

    def reload_service(self) -> bool:
        return self._run_systemctl("reload")

    def force_reload_service(self) -> bool:
        return self._run_systemctl("restart")

    def restart_service(self) -> bool:
        return self._run_systemctl("restart")

    def status_service(self) -> bool:
        return self._run_systemctl("status")

    def execute(self) -> bool:
        commands: dict = {
            "start": self.start_service,
            "stop": self.stop_service,
            "reload": self.reload_service,
            "force_reload": self.force_reload_service,
            "restart": self.restart_service,
            "status": self.status_service
        }
        if self.command in commands:
            return commands[self.command]()
        else:
            print(f"{RED}[!] Error: Unknown command: {self.command}{RESET}")
            return False


class SysVInitManagement:
    """
    A class for managing services using SysVInit.

    This class provides methods to perform basic operations on services,
    such as starting, stopping, reloading, and checking the status. It uses the
    'service' utility to manage services and handles errors that occur during
    command execution.

    Attributes:
        command (str): The command to perform on the service (start, stop, restart, reload, force-reload, status).
        service (str): The name of the service to manage.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command: str = command
        self.service: str = service

    def _run_service(self, action: str) -> bool:
        try:
            subprocess.run(["service", self.service, action], check=True)
            return True
        except subprocess.CalledProcessError as run_service_error:
            print(f"{RED}[!] Error: {run_service_error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_service("start")

    def stop_service(self) -> bool:
        return self._run_service("stop")

    def reload_service(self) -> bool:
        return self._run_service("reload")

    def force_reload_service(self) -> bool:
        return self._run_service("force-reload")

    def restart_service(self) -> bool:
        return self._run_service("restart")

    def status_service(self) -> bool:
        return self._run_service("status")

    def execute(self) -> bool:
        commands: dict = {
            "start": self.start_service,
            "stop": self.stop_service,
            "reload": self.reload_service,
            "force_reload": self.force_reload_service,
            "restart": self.restart_service,
            "status": self.status_service
        }
        if self.command in commands:
            return commands[self.command]()
        else:
            print(f"{RED}[!] Unknown command: {self.command}{RESET}")
            return False


class InitManagement:
    """
    A class for managing services using Init.

    This class provides methods to perform basic operations on services,
    such as starting, stopping, reloading, and checking the status. It uses the
    'service' utility to manage services and handles errors that occur during
    command execution.

    Attributes:
        command (str): The command to perform on the service (start, stop, restart, reload, force-reload, status).
        service (str): The name of the service to manage.

    Take notes:
        Its SysVInit management but with a different name.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command: str = command
        self.service: str = service

    def _run_service(self, action: str) -> bool:
        try:
            subprocess.run(["service", self.service, action], check=True)
            return True
        except subprocess.CalledProcessError as run_service_error:
            print(f"{RED}[!] Error: {run_service_error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_service("start")

    def stop_service(self) -> bool:
        return self._run_service("stop")

    def reload_service(self) -> bool:
        return self._run_service("reload")

    def force_reload_service(self) -> bool:
        return self._run_service("force-reload")

    def restart_service(self) -> bool:
        return self._run_service("restart")

    def status_service(self) -> bool:
        return self._run_service("status")

    def execute(self) -> bool:
        commands: dict = {
            "start": self.start_service,
            "stop": self.stop_service,
            "reload": self.reload_service,
            "force_reload": self.force_reload_service,
            "restart": self.restart_service,
            "status": self.status_service
        }
        if self.command in commands:
            return commands[self.command]()
        else:
            print(f"{RED}[!] Unknown command: {self.command}{RESET}")
            return False


class OpenRCManagement:
    """
    A class for managing services using OpenRC.

    This class provides methods to perform basic operations on services,
    such as starting, stopping, reloading, and checking the status. It uses the
    'rc-service' utility to manage services and handles errors that occur during
    command execution.

    Attributes:
        command (str): The command to perform on the service (start, stop, restart, reload, status).
        service (str): The name of the service to manage.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command: str = command
        self.service: str = service

    def _run_rc(self, action: str) -> bool:
        try:
            subprocess.run(["rc-service", self.service, action], check=True)
            return True
        except subprocess.CalledProcessError as run_rc_error:
            print(f"{RED}[!] Error: {run_rc_error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_rc("start")

    def stop_service(self) -> bool:
        return self._run_rc("stop")

    def reload_service(self) -> bool:
        return self._run_rc("reload")

    def restart_service(self) -> bool:
        return self._run_rc("restart")

    def status_service(self) -> bool:
        return self._run_rc("status")

    def execute(self) -> bool:
        commands: dict = {
            "start": self.start_service,
            "stop": self.stop_service,
            "reload": self.reload_service,
            "restart": self.restart_service,
            "status": self.status_service
        }
        if self.command in commands:
            return commands[self.command]()
        else:
            print(f"{RED}[!] Error: Unknown command: {self.command}{RESET}")
            return False


class S6Management:
    """
    A class for managing services using s6.

    This class provides methods to perform basic operations on services,
    such as starting, stopping, reloading, and checking the status. It uses the
    's6-svc' utility to manage services and handles errors that occur during
    command execution.

    Attributes:
        command (str): The command to perform on the service (start, stop, restart, reload, status).
        service (str): The name of the service to manage.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command: str = command
        self.service: str = service

    def _run_s6_svc(self, action: str) -> bool:
        try:
            subprocess.run(["s6-svc", action, self.service], check=True)
            return True
        except subprocess.CalledProcessError as run_s6_error:
            print(f"{RED}[!] Error: {run_s6_error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_s6_svc("up")

    def stop_service(self) -> bool:
        return self._run_s6_svc("down")

    def reload_service(self) -> bool:
        return self._run_s6_svc("reload")

    def restart_service(self) -> bool:
        return self._run_s6_svc("restart")

    def status_service(self) -> bool:
        return self._run_s6_svc("status")

    def execute(self) -> bool:
        commands: dict = {
            "start": self.start_service,
            "stop": self.stop_service,
            "reload": self.reload_service,
            "restart": self.restart_service,
            "status": self.status_service
        }
        if self.command in commands:
            return commands[self.command]()
        else:
            print(f"{RED}[!] Error: Unknown command: {self.command}{RESET}")
            return False


class RunitManagement:
    """
    A class for managing services using runit.

    This class provides methods to perform basic operations on services,
    such as starting, stopping, reloading, and checking the status. It uses the
    'sv' utility to manage services and handles errors that occur during
    command execution.

    Attributes:
        command (str): The command to perform on the service (start, stop, restart, reload, status).
        service (str): The name of the service to manage.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command: str = command
        self.service: str = service

    def _run_sv(self, action: str) -> bool:
        try:
            subprocess.run(["sv", action, self.service], check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_sv("up")

    def stop_service(self) -> bool:
        return self._run_sv("down")

    def restart_service(self) -> bool:
        return self._run_sv("restart")

    def status_service(self) -> bool:
        return self._run_sv("status")

    def execute(self) -> bool:
        commands: dict = {
            "start": self.start_service,
            "stop": self.stop_service,
            "restart": self.restart_service,
            "status": self.status_service
        }
        if self.command in commands:
            return commands[self.command]()
        else:
            print(f"{RED}[!] Error: Unknown command: {self.command}{RESET}")
            return False


class LaunchdManagement:
    """
    A class for managing services using launchd.

    This class provides methods to perform basic operations on services,
    such as starting, stopping, reloading, and checking the status. It uses the
    'launchctl' utility to manage services and handles errors that occur during
    command execution.

    Attributes:
        command (str): The command to perform on the service (start, stop, restart, reload, status).
        service (str): The name of the service to manage.

    Take notes:
        I don't have any macbook nearby so I can't test it normally.
        This class is probably not working / very unstable.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command: str = command
        self.service: str = service

    def _run_launchctl(self, action: str) -> bool:
        try:
            subprocess.run(["launchctl", action, self.service], check=True)
            return True
        except subprocess.CalledProcessError as run_launchctl_error:
            print(f"{RED}[!] Error: {run_launchctl_error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_launchctl("load")

    def stop_service(self) -> bool:
        return self._run_launchctl("unload")

    def reload_service(self) -> bool:
        return self._run_launchctl("unload") and self._run_launchctl("load")

    def restart_service(self) -> bool:
        return self.reload_service()

    def status_service(self) -> bool:
        try:
            subprocess.run(["launchctl", "list", self.service], check=True)
            return True
        except subprocess.CalledProcessError as launchctl_list_error:
            print(f"{RED}[!] Error: {launchctl_list_error}{RESET}")
            return False

    def execute(self) -> bool:
        commands: dict = {
            "start": self.start_service,
            "stop": self.stop_service,
            "reload": self.reload_service,
            "restart": self.restart_service,
            "status": self.status_service
        }
        if self.command in commands:
            return commands[self.command]()
        else:
            print(f"{RED}[!] Error: Unknown command: {self.command}{RESET}")


class DebianPackageManagement:
    """
    A class for managing packages using apt && dpkg.

    It includes functionality for updating, upgrading, installing, removing, purging and removing unused dependencies.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["apt", "update"], check=True)
            return True
        except subprocess.CalledProcessError as apt_update_error:
            print(f"{RED}[!] Error: {apt_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["apt", "upgrade", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as apt_upgrade_error:
            print(f"{RED}[!] Error: {apt_upgrade_error}{RESET}")
            return False

    @staticmethod
    def full_upgrade() -> bool:
        try:
            subprocess.run(["apt", "upgrade", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as apt_full_upgrade_error:
            print(f"{RED}[!] Error: {apt_full_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apt", "install", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as apt_install_error:
                print(f"{RED}[!] Error: {apt_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apt", "remove", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as apt_remove_error:
                print(f"{RED}[!] Error: {apt_remove_error}{RESET}")
                return False

    @staticmethod
    def purge(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apt", "purge", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as apt_purge_error:
                print(f"{RED}[!] Error: {apt_purge_error}{RESET}")
                return False

    @staticmethod
    def autoremove() -> bool:
        try:
            subprocess.run(["apt", "autoremove", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as apt_autoremove_error:
            print(f"{RED}[!] Error: {apt_autoremove_error}{RESET}")
            return False


class GentooPackageManagement:
    """
    A class for managing packages using portage.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list= packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["emerge", "--sync"], check=True)
            return True
        except subprocess.CalledProcessError as emerge_sync_error:
            print(f"{RED}[!] Error: {emerge_sync_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["emerge", "--update", "--deep", "@world"], check=True)
            return True
        except subprocess.CalledProcessError as emerge_update_deep_world_error:
            print(f"{RED}[!] Error: {emerge_update_deep_world_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["emerge", package], check=True)
                return True
            except subprocess.CalledProcessError as emerge_error:
                print(f"{RED}[!] Error: {emerge_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["emerge", "--depclean", package], check=True)
                return True
            except subprocess.CalledProcessError as emerge_depclean_error:
                print(f"{RED}[!] Error: {emerge_depclean_error}{RESET}")
                return False


class FedoraPackageManagement:
    """
    A class for managing packages using dnf.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["dnf", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as dnf_update_error:
            print(f"{RED}[!] Error: {dnf_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["dnf", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as dnf_upgrade_error:
            print(f"{RED}[!] Error: {dnf_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["dnf", "install", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as dnf_install_error:
                print(f"{RED}[!] Error: {dnf_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["dnf", "remove", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as dnf_remove_error:
                print(f"{RED}[!] Error: {dnf_remove_error}{RESET}")
                return False


class CentOSPackageManagement:
    """
    A class for managing packages using yum.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["yum", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as yum_update_error:
            print(f"{RED}[!] Error: {yum_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["yum", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as yum_upgrade_error:
            print(f"{RED}[!] Error: {yum_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["yum", "install", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as yum_install_error:
                print(f"{RED}[!] Error: {yum_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["yum", "remove", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as yum_remove_error:
                print(f"{RED}[!] Error: {yum_remove_error}{RESET}")
                return False


class OpenSUSEPackageManager:
    """
    A class for managing packages using zypper.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["zypper", "refresh"], check=True)
            return True
        except subprocess.CalledProcessError as zypper_refresh_error:
            print(f"{RED}[!] Error: {zypper_refresh_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["zypper", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as zypper_update_error:
            print(f"{RED}[!] Error: {zypper_update_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["zypper", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as zypper_install_error:
                print(f"{RED}[!] Error: {zypper_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["zypper", "rm", package], check=True)
                return True
            except subprocess.CalledProcessError as zypper_rm_error:
                print(f"{RED}[!] Error: {zypper_rm_error}{RESET}")
                return False


class AlpinePackageManagement:
    """
    A class for managing packages using apk.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["apk", "update"], check=True)
            return True
        except subprocess.CalledProcessError as apk_update_error:
            print(f"{RED}[!] Error: {apk_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["apk", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as apk_upgrade_error:
            print(f"{RED}[!] Error: {apk_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apk", "add", package], check=True)
                return True
            except subprocess.CalledProcessError as apk_add_error:
                print(f"{RED}[!] Error: {apk_add_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apk", "del", package], check=True)
                return True
            except subprocess.CalledProcessError as apk_del_error:
                print(f"{RED}[!] Error: {apk_del_error}{RESET}")
                return False


class VoidPackageManagement:
    """
    A class for managing packages using xbps-install.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["xbps-install", "-S"], check=True)
            return True
        except subprocess.CalledProcessError as xbps_install_s_error:
            print(f"{RED}[!] Error: {xbps_install_s_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["xbps-install", "-u"], check=True)
            return True
        except subprocess.CalledProcessError as xbps_install_u_error:
            print(f"{RED}[!] Error: {xbps_install_u_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["xbps-install", package], check=True)
                return True
            except subprocess.CalledProcessError as xbps_install_error:
                print(f"{RED}[!] Error: {xbps_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["xbps-remove", package], check=True)
                return True
            except subprocess.CalledProcessError as xbps_remove_error:
                print(f"{RED}[!] Error: {xbps_remove_error}{RESET}")
                return False


class DragoraPackageManagement:
    """
    A class for managing packages using qi.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["qi", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as qi_update_error:
            print(f"{RED}[!] Error: {qi_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["qi", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as qi_upgrade_error:
            print(f"{RED}[!] Error: {qi_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["qi", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as qi_install_error:
                print(f"{RED}[!] Error: {qi_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["qi", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as qi_remove_error:
                print(f"{RED}[!] Error: {qi_remove_error}{RESET}")
                return False


class SlackwarePackageManagement:
    """
    A class for managing packages using slackpkg.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["slackpkg", "update"], check=True)
            return True
        except subprocess.CalledProcessError as slackpkg_update_error:
            print(f"{RED}[!] Error: {slackpkg_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["slackpkg", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as slackpkg_upgrade_error:
            print(f"{RED}[!] Error: {slackpkg_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["slackpkg", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as slackpkg_install_error:
                print(f"{RED}[!] Error: {slackpkg_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["slackpkg", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as slackpkg_remove_error:
                print(f"{RED}[!] Error: {slackpkg_remove_error}{RESET}")
                return False


class GuixPackageManagement:
    """
    A class for managing packages using guix.

    It includes functionality for updating, upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["guix", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as guix_update_error:
            print(f"{RED}[!] Error: {guix_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["guix", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as guix_upgrade_error:
            print(f"{RED}[!] Error: {guix_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["guix", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as guix_install_error:
                print(f"{RED}[!] Error: {guix_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["guix", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as guix_remove_error:
                print(f"{RED}[!] Error: {guix_remove_error}{RESET}")
                return False


class ArchPackageManagement:
    """
    A class for managing packages using pacman.

    It includes functionality for updating && upgrading, installing, removing and purging packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update_upgrade() -> bool:
        try:
            subprocess.run(["pacman", "-Syu"], check=True)
            return True
        except subprocess.CalledProcessError as pacman_syu_error:
            print(f"{RED}[!] Error: {pacman_syu_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pacman", "-S", package], check=True)
                return True
            except subprocess.CalledProcessError as pacman_s_error:
                print(f"{RED}[!] Error: {pacman_s_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pacman", "-R", package], check=True)
                return True
            except subprocess.CalledProcessError as pacman_r_error:
                print(f"{RED}[!] Error: {pacman_r_error}{RESET}")
                return False

    @staticmethod
    def purge(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pacman", "-Rns", package], check=True)
                return True
            except subprocess.CalledProcessError as pacman_rns_error:
                print(f"{RED}[!] Error: {pacman_rns_error}{RESET}")
                return False


class FreeBSDPackageManagement:
    """
    A class for managing packages using pkg.

    It includes functionality for updating && upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["pkg", "update"], check=True)
            return True
        except subprocess.CalledProcessError as pkg_update_error:
            print(f"{RED}[!] Error: {pkg_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["pkg", "upgrade", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as pkg_upgrade_error:
            print(f"{RED}[!] Error: {pkg_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg", "install", "-y", package], check=True)
                return True
            except subprocess.CalledProcessError as pkg_install_error:
                print(f"{RED}[!] Error: {pkg_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg", "delete", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as pkg_delete_error:
                print(f"{RED}[!] Error: {pkg_delete_error}{RESET}")
                return False


class OpenBSDPackageManagement:
    """
    A class for managing packages using pkg_add.

    It includes functionality for updating && upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["pkg_add", "-u"], check=True)
            return True
        except subprocess.CalledProcessError as pkg_add_u_error:
            print(f"{RED}[!] Error: {pkg_add_u_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["pkg_add", "-uf"], check=True)
            return True
        except subprocess.CalledProcessError as pkg_add_uf_error:
            print(f"{RED}[!] Error: {pkg_add_uf_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg_add", package], check=True)
                return True
            except subprocess.CalledProcessError as pkg_add_error:
                print(f"{RED}[!] Error: {pkg_add_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg_delete", package], check=True)
                return True
            except subprocess.CalledProcessError as pkg_delete_error:
                print(f"{RED}[!] Error: {pkg_delete_error}{RESET}")
                return False


class NetBSDPackageManagement:
    """
    A class for managing packages using pkgin.

    It includes functionality for updating && upgrading, installing, and removing packages.
    The methods are designed to interact with the system's package manager through subprocess calls and return boolean
    values to indicate success or failure.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro: str = distro
        self.packages: list = packages

    def name(self) -> str:
        return self.distro

    @staticmethod
    def update() -> bool:
        try:
            subprocess.run(["pkgin", "update"], check=True)
            return True
        except subprocess.CalledProcessError as pkgin_update_error:
            print(f"{RED}[!] Error: {pkgin_update_error}{RESET}")
            return False

    @staticmethod
    def upgrade() -> bool:
        try:
            subprocess.run(["pkgin", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as pkgin_upgrade_error:
            print(f"{RED}[!] Error: {pkgin_upgrade_error}{RESET}")
            return False

    @staticmethod
    def install(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkgin", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as pkgin_install_error:
                print(f"{RED}[!] Error: {pkgin_install_error}{RESET}")
                return False

    @staticmethod
    def remove(packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkgin", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as pkgin_remove_error:
                print(f"{RED}[!] Error: {pkgin_remove_error}{RESET}")
                return False


def package_handling(distro: str, package_list: List[str], command: str) -> bool:
    """
    Handles package downloading for different GNU/Linux and BSD distributions.
    """

    print(f"[<==] Installing requirements {package_list}...")
    sleep(1)

    try:
        if command == "install":
            if distro in DEBIAN_BASED:
                debian = DebianPackageManagement(distro, packages=package_list)
                debian.update()
                debian.upgrade()
                debian.install(package_list)
                return True

            elif distro in ARCH_BASED:
                arch = ArchPackageManagement(distro, packages=package_list)
                arch.update_upgrade()
                arch.install(package_list)
                return True

            elif distro in GENTOO_BASED:
                gentoo = GentooPackageManagement(distro, packages=package_list)
                gentoo.update()
                gentoo.upgrade()
                gentoo.install(package_list)
                return True

            elif distro in FEDORA_BASED:
                fedora = FedoraPackageManagement(distro, packages=package_list)
                fedora.update()
                fedora.upgrade()
                fedora.install(package_list)
                return True

            elif distro in CENTOS_BASED:
                centos = CentOSPackageManagement(distro, packages=package_list)
                centos.update()
                centos.upgrade()
                centos.install(package_list)
                return True

            elif distro in ALPINE_BASED:
                alpine = AlpinePackageManagement(distro, packages=package_list)
                alpine.update()
                alpine.upgrade()
                alpine.install(package_list)
                return True

            elif distro in VOID_BASED:
                void = VoidPackageManagement(distro, packages=package_list)
                void.update()
                void.upgrade()
                void.install(package_list)
                return True

            elif distro in DRAGORA_BASED:
                dragora = DragoraPackageManagement(distro, packages=package_list)
                dragora.update()
                dragora.upgrade()
                dragora.install(package_list)
                return True

            elif distro in SLACKWARE_BASED:
                slackware = SlackwarePackageManagement(distro, packages=package_list)
                slackware.update()
                slackware.upgrade()
                slackware.install(package_list)
                return True

            elif distro in GUIX_BASED:
                guix = GuixPackageManagement(distro, packages=package_list)
                guix.update()
                guix.upgrade()
                guix.install(package_list)
                return True

            elif distro in FREEBSD_BASED:
                freebsd = FreeBSDPackageManagement(distro, packages=package_list)
                freebsd.update()
                freebsd.upgrade()
                freebsd.install(package_list)
                return True

            elif distro in OPENBSD_BASED:
                openbsd = OpenBSDPackageManagement(distro, packages=package_list)
                openbsd.update()
                openbsd.upgrade()
                openbsd.install(package_list)
                return True

            elif distro in NETBSD_BASED:
                netbsd = NetBSDPackageManagement(distro, packages=package_list)
                netbsd.update()
                netbsd.upgrade()
                netbsd.install(package_list)
                return True

            else:
                print(f"{RED}[!] Error: Unsupported distribution: {distro}.{RESET}")
                return False

        if command == "remove":
            if distro in DEBIAN_BASED:
                debian = DebianPackageManagement(distro, packages=package_list)
                debian.remove(package_list)
                return True

            elif distro in ARCH_BASED:
                arch = ArchPackageManagement(distro, packages=package_list)
                arch.remove(package_list)
                return True

            elif distro in GENTOO_BASED:
                gentoo = GentooPackageManagement(distro, packages=package_list)
                gentoo.remove(package_list)
                return True

            elif distro in FEDORA_BASED:
                fedora = FedoraPackageManagement(distro, packages=package_list)
                fedora.remove(package_list)
                return True

            elif distro in CENTOS_BASED:
                centos = CentOSPackageManagement(distro, packages=package_list)
                centos.remove(package_list)
                return True

            elif distro in ALPINE_BASED:
                alpine = AlpinePackageManagement(distro, packages=package_list)
                alpine.remove(package_list)
                return True

            elif distro in VOID_BASED:
                void = VoidPackageManagement(distro, packages=package_list)
                void.remove(package_list)
                return True

            elif distro in DRAGORA_BASED:
                dragora = DragoraPackageManagement(distro, packages=package_list)
                dragora.remove(package_list)
                return True

            elif distro in SLACKWARE_BASED:
                slackware = SlackwarePackageManagement(distro, packages=package_list)
                slackware.remove(package_list)
                return True

            elif distro in GUIX_BASED:
                guix = GuixPackageManagement(distro, packages=package_list)
                guix.remove(package_list)
                return True

            elif distro in FREEBSD_BASED:
                freebsd = FreeBSDPackageManagement(distro, packages=package_list)
                freebsd.remove(package_list)
                return True

            elif distro in OPENBSD_BASED:
                openbsd = OpenBSDPackageManagement(distro, packages=package_list)
                openbsd.remove(package_list)
                return True

            elif distro in NETBSD_BASED:
                netbsd = NetBSDPackageManagement(distro, packages=package_list)
                netbsd.remove(package_list)
                return True

            else:
                print(f"{RED}[!] Error: Unsupported distribution: {distro}.{RESET}")
                return False

        if command == "update" or command in "upgrade":
            if distro in DEBIAN_BASED:
                debian = DebianPackageManagement(distro, packages=[])
                debian.update()
                debian.upgrade()
                return True

            elif distro in ARCH_BASED:
                arch = ArchPackageManagement(distro, packages=[])
                arch.update_upgrade()
                return True

            elif distro in GENTOO_BASED:
                gentoo = GentooPackageManagement(distro, packages=[])
                gentoo.update()
                gentoo.upgrade()
                return True

            elif distro in FEDORA_BASED:
                fedora = FedoraPackageManagement(distro, packages=[])
                fedora.update()
                fedora.upgrade()
                return True

            elif distro in CENTOS_BASED:
                centos = CentOSPackageManagement(distro, packages=[])
                centos.update()
                centos.upgrade()
                return True

            elif distro in ALPINE_BASED:
                alpine = AlpinePackageManagement(distro, packages=[])
                alpine.update()
                alpine.upgrade()
                return True

            elif distro in VOID_BASED:
                void = VoidPackageManagement(distro, packages=[])
                void.update()
                void.upgrade()
                return True

            elif distro in DRAGORA_BASED:
                dragora = DragoraPackageManagement(distro, packages=[])
                dragora.update()
                dragora.upgrade()
                return True

            elif distro in SLACKWARE_BASED:
                slackware = SlackwarePackageManagement(distro, packages=[])
                slackware.update()
                slackware.upgrade()
                return True

            elif distro in GUIX_BASED:
                guix = GuixPackageManagement(distro, packages=[])
                guix.update()
                guix.upgrade()
                return True

            elif distro in FREEBSD_BASED:
                freebsd = FreeBSDPackageManagement(distro, packages=[])
                freebsd.update()
                freebsd.upgrade()
                return True

            elif distro in OPENBSD_BASED:
                openbsd = OpenBSDPackageManagement(distro, packages=[])
                openbsd.update()
                openbsd.upgrade()
                return True

            elif distro in NETBSD_BASED:
                netbsd = NetBSDPackageManagement(distro, packages=[])
                netbsd.update()
                netbsd.upgrade()
                return True

            else:
                print(f"{RED}[!] Error: Unsupported distribution: {distro}.{RESET}")
                return False

        if command == "purge":
            if distro in DEBIAN_BASED:
                debian = DebianPackageManagement(distro, packages=package_list)
                debian.purge(package_list)
                return True

            elif distro in ARCH_BASED:
                arch = ArchPackageManagement(distro, packages=package_list)
                arch.purge(package_list)
                return True

            else:
                print(f"{RED}[!] Error: Unsupported distribution: {distro}.{RESET}")
                return False

        if command == "autoremove":
            if distro in DEBIAN_BASED:
                debian = DebianPackageManagement(distro, packages=[])
                debian.autoremove()
                return True

        else:
            print(f"{RED}[!] Error: Unsupported distribution: {distro}.{RESET}")
            return False

    except subprocess.CalledProcessError as package_handling_error:
        print(f"{RED}[!] Error: {package_handling_error}{RESET}")
        return False


def init_system_handling(init_system: str, command: str, service: str) -> bool:
    """
    Handles service management based on the provided init system.

    Args:
        init_system (str): The name of the init system being used
            (e.g., 'systemd', 'sysvinit', 's6').
        command (str): The command to execute for service management
            (e.g., 'enable', 'start', 'stop').
        service (str): The name of the service to manage.

    Returns:
        bool: True if the service management command was executed successfully, False otherwise.
    """

    print(f"[<==] Enabling services [{service}]...")
    sleep(1)

    try:
        if init_system == "systemd":
            _ = SystemdManagement(command, service)
            return True
        elif init_system == "sysvinit":
            _ = SysVInitManagement(command, service)
            return True
        elif init_system == "init":
            _ = InitManagement(command, service)
            return True
        elif init_system == "s6":
            _ = S6Management(command, service)
            return True
        elif init_system == "runit":
            _ = RunitManagement(command, service)
            return True
        elif init_system == "launchd":
            _ = LaunchdManagement(command, service)
            return True
        elif init_system == "openrc":
            _ = OpenRCManagement(command, service)
            return True
        else:
            print(f"{RED}[!] Error: unsupported init system: {init_system}.{RESET}")
            exit(1)

    except subprocess.CalledProcessError as init_system_handling_error:
        print(f"{RED}[!] Error: {init_system_handling_error}{RESET}")
        return False


if __name__ == "__main__":
    the_unix_manager_tester()
