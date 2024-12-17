#!/usr/bin/python3

"""
---------------------------------------
Cheap top/htop analogue.

GNU/Linux supported.
Author: iva
Date: 16.12.2024
---------------------------------------
"""

try:
    import usr
    import subprocess
    from sys import exit
    from os import system
    from time import sleep
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def get_uptime_info() -> str | None:
    try:
        result = subprocess.run(["uptime", "-p"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error fetching uptime: {error}{RESET}")
        return None


def get_disk_info() -> tuple | str | None:
    try:
        result: str = subprocess.run(["df", "-h"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as error:
        print(f"{RED}[!] Error fetching disk information: {error}{RESET}")
        return None


def get_memory_info() -> tuple | str | None:
    try:
        result: str = subprocess.run(["cat", "/proc/meminfo"], capture_output=True, text=True, check=True)
        lines: str = result.stdout.splitlines()
        for line in lines:
            if line.startswith("MemTotal:"):
                total: int = int(line.split()[1]) >> 10
            elif line.startswith("MemFree:"):
                free: int = int(line.split()[1]) >> 10
            elif line.startswith("MemAvailable:"):
                available: int = int(line.split()[1]) >> 10
            elif line.startswith("Buffers:"):
                buffers: int = int(line.split()[1]) >> 10
            elif line.startswith("Cached:"):
                cached: int = int(line.split()[1]) >> 10

        used: int = total - free - buffers - cached
        percent: int = (used / total) * 100 if total > 0 else 0
        
        return total, used, available, percent
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"{RED}[!] Error: {error}{RESET}")
        return None, None, None, None


def process_analysis() -> str:
    system("clear")

    ps_command: str = "ps aux --sort=-%mem | awk 'NR<=5{print $0}'"
    result: subprocess.CompletedProcess = subprocess.run(ps_command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout


def system_monitor() -> None:
    # TODO: finish this module some year.
    while True:
        try:
            system("clear")

            uptime: str = get_uptime_info()
            if uptime is not None:
                print("+-------- UPTIME --------+")
                print(uptime)

            total, used, available, percent = get_memory_info()
            if total is not None:
                print("+-------- MEMORY --------+")
                print(f"Total: {total} MiB\nUsed: {used} MiB")
                print(f"Available: {available} MiB\nUsage: {percent:.1f}%")
                print("-" * 20)

            disk_usage = get_disk_info()
            if disk_usage is not None:
                print("+--------- DISK ---------+")
                print(disk_usage)
            
            processes_info = process_analysis()
            if processes_info is not None:
                print("+------------------------+")
                print(processes_info)
            sleep(1.5)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    system_monitor()
