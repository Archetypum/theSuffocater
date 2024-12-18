#!/usr/bin/python3

"""
---------------------------------------
Setups tor functionality on your machine.

- Installs tor on your machine
- Setups tor nodes.
- Setups Snowflake Proxy on FreeBSD and Debian based GNU/Linux distros
- Setups obfs4 bridges on GNU/Linux and BSD
- Adds Tor repositories for Devuan and Debian GNU/Linux.

Author: iva
Date: 02.12.2024
---------------------------------------
"""

try:
    import usr
    import subprocess
    from os import system
    from time import sleep
    from usr import GREEN, RED, RESET
except ModuleNotFoundError as import_error:
    print(f"{RED}[!] Error: modules not found:\n{import_error}{RESET}")


def install_tor() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    print("We are going to install Tor on your machine.")
    if usr.prompt_user("[?] Proceed?"):
        try:
            usr.package_handling(distro, package_list=["tor", "torsocks"], command="install")
            
            print("Now you need to install Tor Browser from the web.")
            if usr.prompt_user("[?] Proceed?"):
                subprocess.run(["xdg-open", "https://www.torproject.org/download/"], check=True)
            
            print("Looks like you're locked and loaded.")
            print("Tor can't help you if you use it wrong! Learn how to be safe at https://support.torproject.org/faq/staying-anonymous/")
            if usr.prompt_user("[?] Proceed?"):
                subprocess.run(["xdg-open", "https://support.torproject.org/faq/staying-anonymous/"], check=True)
            
            print(f"{GREEN}[*] Success! {RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def snowflake_setup_debian() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro in usr.DEBIAN_BASED_DISTROS:
        print(f"{RED}[!] Error: your OS {distro} in not Debian based.{RESET}")
    
    print(f"{RED}[!] Warning:")
    print("     On Debian Stable based distributions packages might be outdated and so this setup might not work.")
    print(f"     It is recommended to use another setup method, e.g. Docker.{RESET}")

    if usr.prompt_user("[?] Proceed?"):
        print("Snowflake is a pluggable transport available in Tor Browser to defeat internet censorship.") 
        print("Like a Tor bridge, a user can access the open internet when even regular Tor connections are censored.")
        print("To use Snowflake is as easy as to switch to a new bridge configuration in Tor Browser.")
        print("And we are going to setup a docker snowflake proxy for you.")

        if usr.prompt_user("[?] Proceed?"):
            try:
                usr.package_handling(distro, package_list=["snowflake-proxy"], command="install")

                if usr.prompt_user("[?] Start Snowflake service now?"):
                    usr.init_system_handling(init_system, "start", "snowflake-proxy")
                
                print("Looks like you are locked and loaded.\nNow, check snowflake-proxy logs and type")
                print("'systemctl stop snowlake-proxy' or 'service snowflake-proxy stop' if you want to disable it.")
                print(f"{GREEN}[*] Success!{RESET}")
            except (subprocess.CalledProcessError, FileNotFoundError) as error:
                print(f"{RED}[!] Error: {error}{RESET}")


def snowflake_setup_freebsd() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro not in usr.FREEBSD_BASED_DISTROS:
        print(f"{RED}[!] Error: your OS {distro} is not FreeBSD based.{RESET}")
    
    print("Snowflake is a pluggable transport available in Tor Browser to defeat internet censorship.")
    print("Like a Tor bridge, a user can access the open internet when even regular Tor connections are censored.")
    print("To use Snowflake is as easy as to switch to a new bridge configuration in Tor Browser.")
    
    if usr.prompt_user("[?] Proceed?"):
        try:
            usr.package_handling(distro, package_list=["showflake-tor"], command="install")
            
            if usr.prompt_user("[?] Enable Snowflake Proxy daemon on boot and start Snowflake Proxy service now?"):
                subprocess.run(["sysrc", "snowlake_enable=YES"], check=True)
                usr.init_system_handling(init_system, "start", "snowflake")
            
            print("Looks like you are locked and loaded.\nNow, check snowflake-proxy logs and type")
            print("'service snowflake stop' if you want to disable it.")
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def snowflake_setup_docker() -> None:
    system("clear")
    
    distro: str = usr.get_user_distro()
    
    print("Snowflake is a pluggable transport available in Tor Browser to defeat internet censorship.")
    print("Like a Tor bridge, a user can access the open internet when even regular Tor connections are censored.")
    print("To use Snowflake is as easy as to switch to a new bridge configuration in Tor Browser.")
    
    if usr.prompt_user("[?] Proceed?"):
        try:
            usr.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing get-docker.sh...")
            sleep(1)
            subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o get-docker.sh"], check=True)

            print("[<==] Installing docker compose file...")
            sleep(1)
            subprocess.run(["wget", "https://gitlab.torproject.org/tpo/anti-censorship/docker-snowflake-proxy/raw/main/docker-compose.yml", "-O"], check=True)

            if usr.prompt_user("[?] Deploy Snowflake now?"):
                print("[<==] Deploying proxy...")
                sleep(1)
                subprocess.run(["docker", "compose", "up", "-d", "snowflake-proxy"], check=True)
            
            print("Looks like you are locked and loaded. Now, dont forget to check your docker logs:")
            print("- 'docker logs -f snowflake-proxy'")
            print("And update the container with Watchtower:")
            print("- 'docker compose up -d'")
            print(f"{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def torify_apt_devuan() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro != "devuan":
        print(f"{RED}[!] Error: your OS {distro} is not Devuan based.{RESET}")

    print("Tor is a free overlay network for enabling anonymous communication.")
    print("Built on free and open-source software and more than seven thousand volunteer-operated relays worldwide,") 
    print("users can have their Internet traffic routed via a random path through the network.")
    print("And if you wish, you can use apt over tor (Devuan based GNU/Linux distribution required).")

    if usr.prompt_user("[?] Proceed?"):
        try:
            usr.package_handling(distro, package_list=["tor", "apt-transport-tor", "apt-transport-https"], command="install")
            
            if usr.prompt_user("[?] Start tor service now?"):
                usr.init_system_handling(init_system, "start", "tor")
            
            with open("config_files/apt_tor_devuan_repos.txt", "r") as config_file:
                apt_tor_repos: str = config_file.read()

            with open("/etc/apt/sources.list", "a") as true_config_file:
                true_config_file.write(apt_tor_repos)
            
            if usr.prompt_user("[?] View 'sources.list'?"):
                subprocess.run(["nano", "/etc/apt/sources.list"], check=True)
            
            print(f"{GREEN}[*] Success!{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def torify_apt_debian() -> None:
    system("clear")

    distro: str = usr.get_user_distro()
    init_system: str = usr.get_init_system()
    if distro != "debian":
        print(f"{RED}[!] Error: your OS {distro} is not devuan based.{RESET}")

    print("Tor is a free overlay network for enabling anonymous communication.")
    print("Built on free and open-source software and more than seven thousand volunteer-operated relays worldwide,")
    print("users can have their Internet traffic routed via a random path through the network.")
    print("And if you wish, you can use apt over tor (Devuan based GNU/Linux distribution required).")

    if usr.prompt_user("[?] Proceed?"):
        try:
            usr.package_handling(distro, package_list=["tor", "apt-transport-tor", "apt-transport-https"], command="install")
            if usr.prompt_user("[?] Start Tor now?"):
                usr.init_system_handling(init_system, "start", "tor")
                print("[:(] Sorry this function is not implemented yet.\nWe will met again in text stable release.")

            print(f"{GREEN}[*] Success!{RESET}")
        except (subprocess.CalledProcessError, FileNotFoundError, IOError) as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_debian() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")
    
    init_system: str = usr.get_init_system()

    if usr.prompt_user("[?] Proceed?"):
        try:
            package_handling(distro, package_list=["tor", "obfs4proxy"], command="install")
            
            print("[<==] Editing torrc...")
            sleep(1)
            with open("config_files/tor_debian_obfs4.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/tor/torrc", "w") as true_config_file:
                true_config_file.write(config_file_text)

            input("[==>] Hit enter to finish torrc configuration...")
            subprocess.run(["nano", "/etc/tor/torrc"], check=True)
            
            if usr.prompt_user("[?] Start Tor now?"):
                usr.init_system_handling(init_system, "start", "tor")

            print("Looks like you are locked and loaded.\nDon't forget to monitor logs!")
            print("{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_arch() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")
    
    init_system: str = usr.get_init_system()

    if usr.prompt_user("[?] Proceed?"):
        try:
            print("[<==] Installing Tor...")
            sleep(1)
            subprocess.run(["pacman", "-S", "tor"], check=True)

            print("[<==] Building obfs4proxy from source...")
            sleep(1)
            subprocess.run(["git", "clone", "https://aur.archlinux.org/obfs4proxy"], check=True)
            subrocess.run(["cd", "obfs4proxy"], check=True)
            subprocess.run(["makepkg", "-irs"], check=True)
            
            print("[<==] Editing torrc...")
            sleep(1)
            with open("config_files/tor_arch_obfs4.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/tor/torrc", "w") as true_config_file:
                true_config_file.write(config_file_text)

            input("[==>] Hit enter to finish torrc configuration...")
            subprocess.run(["nano", "/etc/tor/torrc"], check=True)

            if usr.prompt_user("[?] Start Tor now?"):
                usr.init_system_handiling(init_system, "start", "tor")
            print("Looks like you are locked and loaded.\nDon't forget to monitor logs!")
            print("{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_void() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    if usr.prompt_user("[?] Proceed?"):
        try:
            print("[<==] Installing Tor && obfs4proxy...")
            sleep(1)
            subprocess.run(["xbps-install", "-S", "tor", "obfs4proxy"], check=True)

            print("[<==] Editing torrc...")
            sleep(1)
            with open("config_files/tor_void_obfs4.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/tor/torrc", "w") as true_config_file:
                true_config_file.write(config_file_text)

            input("[==>] Hit enter to finish torrc configuration...")
            subprocess.run(["nano", "/etc/tor/torrc"], check=True)

            if usr.prompt_user("[?] Start Tor now?"):
                subprocess.run(["ln", "-s", "/etc/sv/tor", "/var/service/."], check=True)
                subprocess.run(["sv", "restart", "tor"], check=True)

            print("Looks like you are locked and loaded.\nDon't forget to monitor logs!")
            print("{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_freebsd() -> None:
    system("clear")
    
    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")
    
    if usr.prompt_user("[?] Proceed?"):
        try:
            print("[<==] Installing Tor && obfs4proxy...")
            sleep(1)
            subprocess.run(["pkg", "install", "tor", "obfs4proxy-tor"], check=True)

            print("[<==] Editing torrc...")
            sleep(1)
            with open("config_files/tor_freebsd_obfs4.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/tor/torrc", "w") as true_config_file:
                true_config_file.write(config_file_text)
            
            subprocess.run(["echo", '"net.inet.ip.random_id=1"', ">>", "/etc/sysctl.conf"], check=True)
            subprocess.run(["sysctl", "net.inet.ip.random_id=1"], check=True)

            input("[==>] Hit enter to finish torrc configuration...")
            subprocess.run(["pico", "/etc/tor/torrc"], check=True)

            if usr.prompt_user("[?] Start Tor now?"):
                subprocess.run(["sysrc", "tor_setuid=YES"], check=True)
                subprocess.run(["sysrc", "tor_enable=YES"], check=True)
                subprocess.run(["service", "tor", "start"], check=True)

            print("Looks like you are locked and loaded.\nDon't forget to monitor logs!")
            print("{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_openbsd() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    if usr.prompt_user("[?] Proceed?"):
        try:
            print("[<==] Installing Tor && obfs4proxy...")
            sleep(1)
            subprocess.run(["pkg_add", "tor", "obfs4proxy"], check=True)

            print("[<==] Editing torrc...")
            sleep(1)
            with open("config_files/tor_openbsd_obfs4.txt", "r") as config_file:
                config_file_text: str = config_file.read()

            with open("/etc/tor/torrc", "w") as true_config_file:
                true_config_file.write(config_file_text)
            
            with open("/etc/login.conf", "w") as true_config_file:
                true_config_file.write("""
tor:\
    :openfiles-max=13500:\
    :tc=daemon:
                                       """)
            subprocess.run(["echo", '"kern.maxfiles=16000"', ">>", "/etc/sysctl.conf"], check=True)
            subprocess.run(["sysctl", "kern.maxfiles=16000"], check=True)

            input("[==>] Hit enter to finish torrc configuration...")
            subprocess.run(["pico", "/etc/tor/torrc"], check=True)
            
            if usr.prompt_user("[?] Start Tor now?"):
                subprocess.run(["rcctl", "enable", "tor"], check=True)
                subprocess.run(["rcctl", "start", "tor"], check=True)

            print("Looks like you are locked and loaded.\nDon't forget to monitor logs!")
            print("{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_netbsd() -> None:
    system("clear")

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")

    if usr.prompt_user("[?] Proceed?"):
        try:
            print("[<==] Setup pkg_add...")
            sleep(1)
            setup_pkg_add_command: str = 'echo "PKG_PATH=http://cdn.netbsd.org/pub/pkgsrc/packages/NetBSD/$(uname -m)/$(uname -r)/All" > /etc/pkg_install.conf'
            subprocess.run([setup_pkg_add_command], check=True)

            print("[<==] Install Tor && obfs4proxy...")
            sleep(1)
            subprocess.run(["pkg_add", "tor", "obfs4proxy"], check=True)
            
            print("[<==] Editing torrc...")
            sleep(1)
            with open("config_files/tor_netbsd_obfs4.txt", "r") as config_file:
                config_file_text: str = config_file.read()
            
            with open("/usr/pkg/etc/tor/torrc", "w") as true_config_file:
                true_config_file.write(config_file_text)
            
            input("[==>] Hit enter to finish torrc configuration...")
            subprocess.run(["pico", "/usr/pkg/etc/tor/torrc"], check=True)
            
            if usr.prompt_user("[?] Start Tor now?"):
                subprocess.run(["ln", "-sf", "/usr/pkg/share/examples/rc.d/tor /etc/rc.d/tor"], check=True)
                subprocess.run(["echo", '"tor=YES"', ">>", "/etc/rc.conf"], check=True)
                subprocess.run(["/etc/rc.d/tor", "start"], check=True)
            
            print("Looks like you are locked and loaded.\nDon't forget to monitor logs!")
            print("{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def obfs4_bridge_docker() -> None:
    system("clear")

    distro: str = usr.get_user_distro()

    print("We are going to setup docker obfs4 bridge to help censored users connect to the Tor network.")
    print("The requirements are:")
    print("- 24/7 Internet connectivity;")
    print("- The ability to expose TCP ports to the Internet (make sure that NAT doesn't get in the way;")
    
    if usr.prompt_user("[?] Proceed?"):
        try:
            usr.package_handling(distro, package_list=[], command="update")

            print("[<==] Installing get-docker.sh...")
            sleep(1)
            subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o get-docker.sh"], check=True)

            print("[<==] Installing docker compose file...")
            sleep(1)
            subprocess.run(["wget", "https://gitlab.torproject.org/tpo/anti-censorship/docker-obfs4-bridge/-/raw/main/docker-compose.yml"], check=True)

            subprocess.run(["touch", ".env"], check=True)
            tor_port: str = input("[==>] Your bridge's Tor port: ").strip()
            obfs4_port: str = input("[==>] Your bridge's obfs4 port: ").strip()
            email: str = input("[==>] Your Email: ").strip()

            dotenv_template: str = f"""
# Your bridge's Tor port.
OR_PORT={tor_port}
# Your bridge's obfs4 port.
PT_PORT={obfs4_port}
# Your email address.
EMAIL={email}"""
            
            with open(".env", "w") as config_file:
                config_file.write(dotenv_template)

            if usr.prompt_user("[?] Deploy container now?"):
                print("[<==] Deploying bridge...")
                sleep(1)
                subprocess.run(["docker-compose", "up", "-d", "obfs4-bridge"], check=True)

                print("Looks like you are locked and loaded. Now, dont forget to check your docker logs:")
                print("- 'docker logs CONTAINER_ID'")
                print("And update the container:")
                print("- 'docker-compose pull obfs4-bridge'")
                print(f"{GREEN}[*] Success!{RESET}")
        except subprocess.CalledProcessError as error:
            print(f"{RED}[!] Error: {error}{RESET}")


def tor_node_setup() -> None:
    system("clear")
    
    print("Not implemented yet.\nWe will meet again in the next stable release.")


def tor_management() -> None:
    system("clear")

    functions: dict = {
            "install_tor": install_tor,
            "torify_apt_debian": torify_apt_debian,
            "torify_apt_devuan": torify_apt_devuan,
            "obfs4_bridge_debian": obfs4_bridge_debian,
            "obfs4_bridge_arch": obfs4_bridge_arch,
            "obfs4_bridge_void": obfs4_bridge_void,
            "obfs4_bridge_freebsd": obfs4_bridge_freebsd,
            "obfs4_bridge_openbsd": obfs4_bridge_openbsd,
            "obfs4_bridge_netbsd": obfs4_bridge_netbsd,
            "obfs4_bridge_docker": obfs4_bridge_docker,
            "snowflake_setup_debian": snowflake_setup_debian,
            "snowflake_setup_freebsd": snowflake_setup_freebsd,
            "tor_node_setup": tor_node_setup
            }

    print("+---- Tor Management  ----+")
    print("\nAvailable functions:")
    for function in functions.keys():
        print(f" - {function}")

    your_function: str = input("[==>] Enter function: ").lower()
    if your_function in functions:
        functions[your_function]()


if __name__ == "__main__": 
    tor_management()
