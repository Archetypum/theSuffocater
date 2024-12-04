#!/usr/bin/python3

"""
Here you can find list of common functions
used by theSuffocater.

Required by all theSuffocater modules

Author: iva
Date: 26.11.2024
"""

###### Fancy color codes ;3 ######
GREEN: str = "\033[92m"
RED: str = "\033[91m"
RESET: str = "\033[0m"

###### GNU/LINUX ######
DEBIAN_BASED_DISTROS: list = ["debian", "ubuntu", "xubuntu", "mint", "lmde", "trisquel", "devuan", 
                              "kali", "parrot", "pop", "elementary", "mx", "antix", "crunchbag",
                              "crunchbag++", "pure", "deepin", "zorin", "peppermint", "lubuntu",
                              "kubuntu", "wubuntu", "steamos", "astra", "tails"]
ARCH_BASED_DISTROS: list = ["arch", "artix", "manjaro", "endeavour", "garuda", "parabola", "hyperbola", "blackarch", "librewolf"]
ALPINE_BASED_DISTROS: list = ["alpine", "postmarket"]
GENTOO_BASED_DISTROS: list = ["gentoo", "pentoo", "funtoo", "calculate" "chrome"]
VOID_BASED_DISTROS: list = ["void", "argon", "shikake", "pristine"]
DRAGORA_BASED_DISTROS: list = ["dragora"]
SLACKWARE_BASED_DISTROS: list = ["slackware"]
FEDORA_BASED_DISTROS: list = ["fedora", "mos"]
CENTOS_BASED_DISTROS: list = ["centos"]
GUIX_BASED_DISTROS: list = ["guix"]
UTUTO_BASED_DISTROS: list = ["ututo"]
CENTOS_BASED_DISTROS: list = ["centos"]

###### BSD ######
FREEBSD_BASED_DISTROS: list = ["freebsd", "midnightbsd", "ghostbsd", "bastillebsd", "cheribsd", "dragonflybsd", "trueos",
                               "hardenedbsd", "hellosystem", "truenas"]
OPENBSD_BASED_DISTROS: list = ["openbsd", "adj", "libertybsd"]
NETBSD_BASED_DISTROS: list = ["netbsd", "blackbsd", "edgebsd"]

try:
    import os
    import subprocess
    from sys import exit
    from time import sleep
    from typing import List
except ModuleNotFoundError:
    print(f"{RED}Error: python modules not found.\nBroken installation?{RESET}")


def tester() -> None:
    os.system("clear")
    
    functions: dict = {
            "get_user_distro": get_user_distro,
            "get_init_system": get_init_system,
            "is_debian_based": is_debian_based,
            "is_arch_based": is_arch_based
            }

    print("Available functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function name (or anything to leave) >>> ").lower()
    if your_function in functions:
        functions[your_function]()


def get_user_distro() -> str:
    """
    Detects user GNU/Linux or BSD distribution.
    Detects probably everything.
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
        print(f"{RED}[!] Error: Cannot detect distribution from /etc/os-release.{RESET}")
        name: str = input("[==>] Write the base of your OS yourself: ").strip().lower()

        return name


def is_debian_based(distro: str) -> True:
    """
    Detects if provided distro is debian based.
    """

    return True if distro in DEBIAN_BASED_DISTROS else False


def is_arch_based(distro: str) -> str:
    """
    Detects if provided distro is arch based.
    """

    return True if distro is ARCH_BASED_DISTROS else False


def get_init_system() -> str:
    """
    Detects init system.
    Can detect ugly fucking systemd, sysvinit, openrc, s6, init, and launchd.

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

    try:
        init_pid = subprocess.check_output(["ps", "-p", "1", "-o", "comm="]).decode().strip()
        if init_pid == "init":
            return "sysvinit"  # init is almost identical to sysvinit
    except subprocess.CalledProcessError:
        pass

    return "unknown"


class SysVInitManagement:
    """
    Simple class for working with service in your modules.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command = command
        self.service = service

    def _run_service_command(self, action: str) -> bool:
        try:
            subprocess.run(["service", self.service, action], check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_service_command("start")

    def stop_service(self) -> bool:
        return self._run_service_command("stop")
    
    def reload_service(self) -> bool:
        return self._run_service_command("reload")

    def force_reload_service(self) -> bool:
        return self._run_service_command("force-reload")

    def restart_service(self) -> bool:
        return self._run_service_command("restart")
    
    def status_service(self) -> bool:
        return self._run_service_command("status")

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


class SystemdManagement:
    """
    Simple class for working with systemctl.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command = command
        self.service = service

    def _run_systemctl(self, action: str) -> bool:
        try:
            subprocess.run(["systemctl", action, self.service], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
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


class OpenRCManagement:
    """
    Simple class for working with rc-service.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command = command
        self.service = service

    def _run_rc_service(self, action: str) -> bool:
        try:
            subprocess.run(["rc-service", self.service, action], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_rc_service("start")

    def stop_service(self) -> bool:
        return self._run_rc_service("stop")
    
    def reload_service(self) -> bool:
        return self._run_rc_service("reload")

    def restart_service(self) -> bool:
        return self._run_rc_service("restart")
    
    def status_service(self) -> bool:
        return self._run_rc_service("status")

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
    Simple class for working with s6-svc.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command = command
        self.service = service

    def _run_s6_svc(self, action: str) -> bool:
        try:
            subprocess.run(["s6-svc", action, self.service], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_s6_svc("up")

    def stop_service(self) -> bool:
        return self._run_s6_svc("down")
    
    def reload_service(self) -> bool:
        return self._run_s6_svc("reload")

    def force_reload_service(self) -> bool:
        return self._run_s6_svc("restart")

    def restart_service(self) -> bool:
        return self._run_s6_svc("restart")
    
    def status_service(self) -> bool:
        return self._run_s6_svc("status")

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


class LaunchdManagement:
    """
    Simple class for working with launchctl.
    """

    def __init__(self, command: str, service: str) -> None:
        self.command = command
        self.service = service

    def _run_launchctl(self, action: str) -> bool:
        try:
            subprocess.run(["launchctl", action, self.service], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def start_service(self) -> bool:
        return self._run_launchctl("load")

    def stop_service(self) -> bool:
        return self._run_launchctl("unload")

    def reload_service(self) -> bool:
        # on mac os reload is handled by unloading and loading again..
        return self._run_launchctl("unload") and self._run_launchctl("load")

    def force_reload_service(self) -> bool:
        return self.reload_service()

    def restart_service(self) -> bool:
        return self.reload_service()

    def status_service(self) -> bool:
        try:
            subprocess.run(["launchctl", "list", self.service], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

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
            print(f"{RED}Error: Unknown command: {self.command}{RESET}")


class DebianPackageManagement:
    """
    Simple class for working with apt in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["apt", "update"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False
    
    def upgrade(self) -> bool:
        try:
            subprocess.run(["apt", "upgrade", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False
    
    def full_upgrade(self) -> bool:
        try:
            subprocess.run(["apt", "full-upgrade", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apt", "install", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False
    
    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apt", "remove", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False
    
    def purge(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apt", "purge", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def autoremove(self) -> bool:
        try:
            subprocess.run(["apt", "autoremove", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False


class GentooPackageManagement:
    """
    Simple class for working with portage in your modules.
    """
    
    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro
    
    def update(self) -> bool:
        try:
            subprocess.run(["emerge", "--sync"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["emerge", "--update", "--deep", "@world"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["emerge", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["emerge", "--depclean", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class FedoraPackageManagement:
    """
    Simple class for working with ugly fucking dnf in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = package
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["dnf", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["dnf", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["dnf", "install", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["dnf", "remove", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class CentOSPackageManagement:
    """
    Simple class for working with yum in your modules.
    """

    def __init__(self, distro: str, package: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["yum", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["yum", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["yum", "install", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["yum", "remove", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class OpenSUSEPackageManager:
    """
    Simple class for working with zypper in your modules
    """
    
    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["zypper", "refresh"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["zypper", "update", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["zypper", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["zypper", "rm", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class AlpinePackageManagement:
    """
    Simple class for working with apk in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro =  distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["apk", "update"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["apk", "upgrade", "-U", "-a"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apk", "add", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {error}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["apk", "del", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {error}{RESET}")
                return False


class VoidPackageManagement:
    """
    Simple class for working with xbps in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["xbps-install", "-S"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["xbps-install", "-u"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["xbps-install", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["xbps-remove", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class DragoraPackageManagement:
    """
    Simple class for working with qi in your modules.
    """
    
    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["qi", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["qi", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["qi", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["qi", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class SlackwarePackageManagement:
    """
    Simple class for working with slackpkg in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["slackpkg", "update"], check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["slackpkg", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["slackpkg", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["slackpkg", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {error}{RESET}")
                return False


class GuixPackageManager:
    """
    Simple class for working with guix in your modules.
    """ 

    def __init__(self, distro: str, package: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["guix", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["guix", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, package: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["guix", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, package: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["guix", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class ArchPackageManagement:
    """
    Simple class for working with pacman in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages

    def name(self) -> str:
        return self.distro
    
    def update_upgrade(self) -> bool:
        try:
            subprocess.run(["pacman", "-Syu"], check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")
            return False
    
    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pacman", "-S", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {error}{RESET}")
                return False
    
    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pacman", "-R", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def purge(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pacman", "-Rns", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class FreeBSDPackageManagement:
    """
    Simple class for working with pkg in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["pkg", "update"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["pkg", "upgrade", "-y"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg", "install", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg", "delete", package, "-y"], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False


class OpenBSDPackageManagement:
    """
    Simple class for working with pkg_add in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["pkg_add", "-u"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["pkg_add", "-uf"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}[!] Error: {e}{RESET}")
            return False
    
    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg_add", package], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"{RED}[!] Error: {e}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkg_delete", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {error}{RESET}")
                return False


class NetBSDPackageManagement:
    """
    Simple class for working with pkgin in your modules.
    """

    def __init__(self, distro: str, packages: List[str]) -> None:
        self.distro = distro
        self.packages = packages
    
    def name(self) -> str:
        return self.distro

    def update(self) -> bool:
        try:
            subprocess.run(["pkgin", "update"], check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")
            return False

    def upgrade(self) -> bool:
        try:
            subprocess.run(["pkgin", "upgrade"], check=True)
            return True
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")
            return False
    
    def install(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkgin", "install", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {error}{RESET}")
                return False

    def remove(self, packages: List[str]) -> bool:
        for package in packages:
            try:
                subprocess.run(["pkgin", "remove", package], check=True)
                return True
            except subprocess.CalledProcessError as error:
                print(f"{RED}[!] Error: {error}{RESET}")
                return False


def package_handling(distro: str, package_list: List[str], command: str) -> bool:
    """
    Handles package downloading for different GNU/Linux and BSD distributions.
    """

    print(f"[<==] Installing requirements {package_list}...")
    sleep(1)

    try:
        if command == "install":
            if distro in DEBIAN_BASED_DISTROS:
                debian = DebianPackageManagement(distro, packages=package_list)
                debian.update()
                debian.upgrade()
                debian.install(package_list)
                return True

            elif distro in ARCH_BASED_DISTROS:
                arch = ArchPackageManagement(distro, packages=package_list)
                arch.update_upgrade()
                arch.install(package_list)
                return True

            elif distro in GENTOO_BASED_DISTROS:
                gentoo = GentooPackageManagement(distro, packages=package_list)
                gentoo.update()
                gentoo.upgrade()
                gentoo.install(package_list)
                return True

            elif distro in FEDORA_BASED_DISTROS:
                fedora = FedoraPackageManagement(distro, packages=package_list)
                fedora.update()
                fedora.upgrade()
                fedora.install(package_list)
                return True

            elif distro in CENTOS_BASED_DISTROS:
                centos = CentOSPackageManagement(distro, packages=package_list)
                centos.update()
                centos.upgrade()
                centos.install(package_list)
                return True

            elif distro in ALPINE_BASED_DISTROS:
                alpine = AlpinePackageManagement(distro, packages=package_list)
                alpine.update()
                alpine.upgrade()
                alpine.install(package_list)
                return True

            elif distro in VOID_BASED_DISTROS:
                void = VoidPackageManagement(distro, packages=package_list)
                void.update()
                void.upgrade()
                void.install(package_list)
                return True

            elif distro in DRAGORA_BASED_DISTROS:
                dragora = DragoraPackageManagement(distro, packages=package_list)
                dragora.update()
                dragora.upgrade()
                dragora.install(package_list)
                return True

            elif distro in SLACKWARE_BASED_DISTROS:
                slackware = SlackwarePackageManagement(distro, packages=package_list)
                slackware.update()
                slackware.upgrade()
                slackware.install(package_list)
                return True

            elif distro in GUIX_BASED_DISTROS:
                guix = GuixPackageManagement(distro, packages=package_list)
                guix.update()
                guix.upgrade()
                guix.install(package_list)
                return True

            elif distro in UTUTO_BASED_DISTROS:
                ututo = UtutoPackageManagement(distro, packages=package_list)
                ututo.update()
                ututo.upgrade()
                ututo.install(package_list)
                return True

            elif distro in FREEBSD_BASED_DISTROS:
                freebsd = FreeBSDPackageManagement(distro, packages=package_list)
                freebsd.update()
                freebsd.upgrade()
                freebsd.install(package_list)
                return True

            elif distro in OPENBSD_BASED_DISTROS:
                openbsd = OpenBSDPackageManagement(distro, packages=package_list)
                openbsd.update()
                openbsd.upgrade()
                openbsd.install(package_list)
                return True

            elif distro in NETBSD_BASED_DISTROS:
                netbsd = NetBSDPackageManagement(distro, packages=package_list)
                netbsd.update()
                netbsd.upgrade()
                netbsd.install(package_list)
                return True

            else:
                print(f"{RED}[!] Unsupported distribution: {distro}.{RESET}")
                return False
        
        if command == "remove":
            if distro in DEBIAN_BASED_DISTROS:
                debian = DebianPackageManagement(distro, packages=package_list)
                debian.remove(package_list)
                return True

            elif distro in ARCH_BASED_DISTROS:
                arch = ArchPackageManagement(distro, packages=package_list)
                arch.remove(package_list)
                return True

            elif distro in GENTOO_BASED_DISTROS:
                gentoo = GentooPackageManagement(distro, packages=package_list)
                gentoo.remove(package_list)
                return True

            elif distro in FEDORA_BASED_DISTROS:
                fedora = FedoraPackageManagement(distro, packages=package_list)
                fedora.remove(package_list)
                return True

            elif distro in CENTOS_BASED_DISTROS:
                centos = CentOSPackageManagement(distro, packages=package_list)
                centos.remove(package_list)
                return True

            elif distro in ALPINE_BASED_DISTROS:
                alpine = AlpinePackageManagement(distro, packages=package_list)
                alpine.remove(package_list)
                return True

            elif distro in VOID_BASED_DISTROS:
                void = VoidPackageManagement(distro, packages=package_list)
                void.remove(package_list)
                return True

            elif distro in DRAGORA_BASED_DISTROS:
                dragora = DragoraPackageManagement(distro, packages=package_list)
                dragora.remove(package_list)
                return True

            elif distro in SLACKWARE_BASED_DISTROS:
                slackware = SlackwarePackageManagement(distro, packages=package_list)
                slackware.remove(package_list)
                return True

            elif distro in GUIX_BASED_DISTROS:
                guix = GuixPackageManagement(distro, packages=package_list)
                guix.remove(package_list)
                return True

            elif distro in UTUTO_BASED_DISTROS:
                ututo = UtutoPackageManagement(distro, packages=package_list)
                ututo.remove(package_list)
                return True

            elif distro in FREEBSD_BASED_DISTROS:
                freebsd = FreeBSDPackageManagement(distro, packages=package_list)
                freebsd.remove(package_list)
                return True

            elif distro in OPENBSD_BASED_DISTROS:
                openbsd = OpenBSDPackageManagement(distro, packages=package_list)
                openbsd.remove(package_list)
                return True

            elif distro in NETBSD_BASED_DISTROS:
                netbsd = NetBSDPackageManagement(distro, packages=package_list)
                netbsd.remove(package_list)
                return True

            else:
                print(f"{RED}[!] Error: Unsupported distribution: {distro}.{RESET}")
                return False
        
        if command == "update" or command in "upgrade":
            if distro in DEBIAN_BASED_DISTROS:
                debian = DebianPackageManagement(distro, packages=[])
                debian.update()
                debian.upgrade()
                return True

            elif distro in ARCH_BASED_DISTROS:
                arch = ArchPackageManagement(distro, packages=[])
                arch.update_upgrade()
                return True

            elif distro in GENTOO_BASED_DISTROS:
                gentoo = GentooPackageManagement(distro, packages=[])
                gentoo.update()
                gentoo.upgrade()
                return True

            elif distro in FEDORA_BASED_DISTROS:
                fedora = FedoraPackageManagement(distro, packages=[])
                fedora.update()
                fedora.upgrade()
                return True

            elif distro in CENTOS_BASED_DISTROS:
                centos = CentOSPackageManagement(distro, packages=[])
                centos.update()
                centos.upgrade()
                return True

            elif distro in ALPINE_BASED_DISTROS:
                alpine = AlpinePackageManagement(distro, packages=[])
                alpine.update()
                alpine.upgrade()
                return True

            elif distro in VOID_BASED_DISTROS:
                void = VoidPackageManagement(distro, packages=[])
                void.update()
                void.upgrade()
                return True

            elif distro in DRAGORA_BASED_DISTROS:
                dragora = DragoraPackageManagement(distro, packages=[])
                dragora.update()
                dragora.upgrade()
                return True

            elif distro in SLACKWARE_BASED_DISTROS:
                slackware = SlackwarePackageManagement(distro, packages=[])
                slackware.update()
                slackware.upgade()
                return True

            elif distro in GUIX_BASED_DISTROS:
                guix = GuixPackageManagement(distro, packages=[])
                guix.update()
                guix.upgrade()
                return True

            elif distro in UTUTO_BASED_DISTROS:
                ututo = UtutoPackageManagement(distro, packages=[])
                ututo.update()
                ututo.upgrade()
                return True

            elif distro in FREEBSD_BASED_DISTROS:
                freebsd = FreeBSDPackageManagement(distro, packages=[])
                freebsd.update()
                freebsd.upgrade()
                return True

            elif distro in OPENBSD_BASED_DISTROS:
                openbsd = OpenBSDPackageManagement(distro, packages=[])
                openbsd.update()
                openbsd.upgrade()
                return True

            elif distro in NETBSD_BASED_DISTROS:
                netbsd = NetBSDPackageManagement(distro, packages=[])
                netbsd.update()
                netbsd.upgrade()
                return True

            else:
                print(f"{RED}[!] Error: Unsupported distribution: {distro}.{RESET}")
                return False

    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error: {error}{RESET}")
        return False


def init_system_handling(init_system: str, command: str, service: str) -> bool:
    """
    Handles services for GNU/Linux and BSD distributions. 
    """

    print(f"[<==] Enabling services [{service}]...")
    sleep(1)
    
    try:
        if init_system == "systemd":
            systemctl = SystemdManagement(command, service)
        elif init_system == "sysvinit" or init_system == "init":
            service = SysVInitManagement(command, service)
        elif init_system == "s6":
            s6_svc = S6Management(command, service)
        elif init_system == "launchd":
            launchctl = LaunchdManagement(command, service)
        elif init_system == "openrc":
            rc_service = OpenRCManagement(command, service)
        else:
            print(f"{RED}[!] Error: unsupported init system.{RESET}")
            exit(1)

    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error: {error}{RESET}")
        return False


if __name__ == "__main__":
    init_system: str = get_init_system()
    distro: str = get_user_distro()
    
    print(distro)
    print(init_system)

    package_handling(distro, package_list=["vim"], command="update")
    # package_handling(distro, package_list=["vrms", "htop"], command="install")
    # package_handling(distro, package_list=["vrms"], command="remove")
