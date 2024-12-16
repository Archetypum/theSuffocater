#!/bin/bash

clear

# Fancy color codes ;3
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"

GUIX_BASED_DISTROS=("guix")
REDHAT_BASED_DISTROS=("redhat")
CENTOS_BASED_DISTROS=("centos" "oracle")
FEDORA_BASED_DISTROS=("fedora" "rocky" "mos")
DRAGORA_BASED_DISTROS=("dragora")
OPENSUSE_BASED_DISTROS=("opensuse")
SLACKWARE_BASED_DISTROS=("slackware")
ALPINE_BASED_DISTROS=("alpine" "postmarket")
VOID_BASED_DISTROS=("void" "argon" "shikake" "pristine")
GENTOO_BASED_DISTROS=("gentoo" "funtoo" "calculate" "chromeos")
OPENBSD_BASED_DISTROS=("openbsd" "adj" "libertybsd")
NETBSD_BASED_DISTROS=("netbsd" "blackbsd" "edgebsd")
FREEBSD_BASED_DISTROS=("freebsd" "ghostbsd" "midnightbsd" "bastillebsd" "cheribsd" "trueos" "dragonflybsd" "hardenedbsd" "hellosystem" "truenas")
ARCH_BASED_DISTROS=("arch" "artix" "manjaro" "garuda" "hyperbola" "parabola" "endeavouros" "blackarch" "librewolfos")
DEBIAN_BASED_DISTROS=("debian" "ubuntu" "xubuntu" "kubuntu" "mint" "lmde" "trisquel" "devuan" "kali" 
	"parrot" "pop" "elementary" "mx" "antix" "steamos" "tails" "astra" "crunchbag"
	"crunchbag++" "pureos" "deepin" "zorin" "peppermintos" "lubuntu" "wubuntu"
	)
	
echo "Supported Platforms:"
for ELEMENT in "${GUIX_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${REDHAT_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${CENTOS_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${FEDORA_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${DRAGORA_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${OPENSUSE_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${SLACKWARE_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${ALPINE_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${VOID_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${GENTOO_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${OPENBSD_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${NETBSD_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${FREEBSD_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${ARCH_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done 
for ELEMENT in "${DEBIAN_BASED_DISTROS[@]}"; do echo " - $ELEMENT"; done

function list_of_packages() {
	PACKAGES=("python3" "python3-pip"
		"net-tools" "ufw" "iptables" "nftables" "fail2ban"
		"openvpn" "wireguard/wireguard-tools"
		"git" "wget" "lsof" "bash" "unbound"
	)

	echo "Packages to install:"
	for ELEMENT in "${PACKAGES[@]}"; do 
		echo " - $ELEMENT" 
	done
}

function install_python_requirements() {
	python3 -m venv pkgenv
	source pkgenv/bin/activate
	pip install -r python_requirements.txt
		
	echo "Don't forget to 'source pkgenv/bin/activate' and you are good to go."
	echo -e "${GREEN}[*] Success!${RESET}"
}

function install_python_requirements_netbsd() {
	python3.12 -m venv pkgenv
	. pkgenv/bin/activate
	pip install -r python_requirements.txt

	echo "Don't forget to 'source' pkgenv/bin/activate and you are good to go."
	echo -e "${GREEN}[*] Success!${RESET}"
}

function install_debian_based() {
	apt update && apt full-upgrade -y
	apt install python3 python3-pip -y
	apt install net-tools iproute2 ufw iptables fail2ban nftables -y
	apt install openvpn wireguard wireguard-tools -y
	apt install lsof git wget bash curl unbound passwd -y
}

function install_arch_based() {
	pacman -Syu --noconfirm
	pacman -S python python-pip tk --noconfirm
	pacman -S net-tools iproute2 ufw iptables nftables fail2ban --noconfirm
	pacman -S openvpn wireguard-tools --noconfirm
	pacman -S lsof git wget bash curl unbound shadow --noconfirm
}

function install_gentoo_based() {
	emerge --sync && emerge --update --deep @world
	emerge python python-pip tk
	emerge net-tools iproute2 ufw iptables nftables fail2ban
	emerge openvpn wireguard-tools
	emerge lsof git wget bash curl unbound
}

function install_alpine_based() {
	apk update && apk upgrade
	apk add python3 py3-pip
	apk add net-tools iproute2 ufw iptables nftables fail2ban
	apk add wireguard-tools openvpn
	apk add lsof git wget bash curl unbound
}

function install_void_based() {
	xbps-install -Su
	xbps-install python3 python3-pip
	xbps-install net-tools iproute2 ufw iptables nftables fail2ban
	xbps-install openvpn wireguard-tools
	xbps-install lsof git wget bash curl unbound
}

function install_fedora_based() {
	dnf update -y
	dnf install python3 python3-pip -y
	dnf install net-tools iproute2 firewalld iptables-services nftables fail2ban -y
	dnf install openvpn wireguard-tools -y
	dnf install lsof git wget bash curl unbound -y
}

function install_opensuse_based() {
	zypper refresh && zypper update -y
	zypper install -y python3 python3-pip
	zypper install -y net-tools iproute2 firewalld iptables nftables fail2ban
	zypper install -y openvpn wireguard-tools
	zypper install -y lsof git wget bash curl unbound
}

function install_slackware_based() {
	slackpkg update && slackpkg upgrade
	slackpkg install python3 python3-pip
	slackpkg install net-tools iproute2 ufw iptables nftables fail2ban
	slackpkg install openvpn wireguard-tools
	slackpkg install lsof git wget bash curl unbound
}

function install_redhat_based() {
	yum update && yum upgrade -y
	yum install python3 python3-pip -y
	yum install net-tools iproute2 firewalld iptables-services nftables fail2ban -y
	yum install openvpn wireguard-tools -y
	yum install lsof git wget bash curl unbound shadow-utils -y
}

function install_freebsd_based() {
	pkg update && pkg upgrade -y
	pkg install -y python3 py3-pip
	pkg install -y py311-fail2ban
	pkg install -y openvpn wireguard-tools
	pkg install -y lsof git wget bash curl unbound bsdadminscripts

	echo -e "${RED}[!] Warning:"
	echo "    Iptables, nftables, Iproute, and ufw are GNU/Linux specific tools."
	echo "    To achieve similar functionality, use tools designed for BSD systems,"
	echo -e "    like PF (Packet Filter), IPFilter (ipf), or build these packages yourself.${RESET}"
	echo -n "[==>] Hit enter to proceed: "
	read PROCEED
}

function install_netbsd_based() {
	pkgin update && pkgin upgrade
	pkgin install python3.12
	python3.12 -m ensurepip --upgrade
	pkgin install fail2ban
	pkgin install lsof git wget bash
	pkgin install openvpn wireguard-tools curl unbound shadow

	echo -e "${RED}[!] Warning:"
	echo "    Iptables, nftables, Iproute, and ufw are GNU/Linux specific tools."
	echo "    To achieve similar functionality, use tools designed for BSD systems,"
	echo -e "    like PF (Packet Filter), IPFilter (ipf), or build these packages yourself.${RESET}"
	echo -n "[==>] Hit enter to proceed: "
	read PROCEED
}

function install_openbsd_based() {
	pkg_add -u
	pkg_add -uf
	pkg_add python3 py3-pip
	pkg_add iproute2 pfctl fail2ban
	pkg_add openvpn wireguard-tools
	pkg_add lsof git wget bash curl unbound bsdadminscripts

	echo -e "${RED}[!] Warning:"
	echo "    Iptables, nftables, Iproute, and ufw are GNU/Linux specific tools."
	echo "    To achieve similar functionality, use tools designed for BSD systems,"
	echo -e "    like PF (Packet Filter), IPFilter (ipf), or build these packages yourself.${RESET}"
	echo -n "[==>] Hit enter to proceed: "
	read PROCEED
}

function install_dragora_based() {
	qi upgrade 
	qi install python3 python3-pip
	qi install net-tools iproute2 ufw iptables nftables fail2ban
	qi install openvpn wireguard-tools
	qi install lsof git wget bash curl unbound
}

function install_guix_based() {
	guix upgrade
	guix install python3 python3-pip
	guix install net-tools iproute2 ufw iptables nftables fail2ban
	guix install openvpn wireguard-tools
	guix install lsof git wget curl unbound
}

function to_lowercase() {
	echo "$1" | tr "[:upper:]" "[:lower:]"
}

function main() {
	echo -n "[==>] Enter the base of your GNU/Linux or BSD distribution ('packages' to view requirements): "
	read DISTRO
	if [[ "$DISTRO" == "packages" ]]; then
		list_of_packages
		main
		return
	fi

	DISTRO=$(to_lowercase "$DISTRO")
	echo "[<==] Installing requirements..."
	echo "--------------------------------------------------------------------------------------"

	for ITEM in "${DEBIAN_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_debian_based
			break
		fi
	done
	
	for ITEM in "${ARCH_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_arch_based
			break
		fi
	done
	
	for ITEM in "${GUIX_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_guix_based
			break
		fi
	done
	
	for ITEM in "${REDHAT_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_redhat_based
			break
		fi
	done

	for ITEM in "${CENTOS_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_redhat_based
			break
		fi
	done

	for ITEM in "${FEDORA_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_fedora_based
			break
		fi
	done

	for ITEM in "${DRAGORA_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_dragora_based
			break
		fi
	done

	for ITEM in "${OPENSUSE_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_opensuse_based
			break
		fi
	done

	for ITEM in "${SLACKWARE_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_slackware_based
			break
		fi
	done

	for ITEM in "${ALPINE_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_alpine_based
			break
		fi
	done

	for ITEM in "${VOID_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_void_based
			break
		fi
	done

	for ITEM in "${GENTOO_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_gentoo_based
			break
		fi
	done

	for ITEM in "${OPENBSD_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_openbsd_based
			break
		fi
	done

	for ITEM in "${NETBSD_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_netbsd_based
			install_python_requirements_netbsd
			exit 0
		fi
	done

	for ITEM in "${FREEBSD_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_freebsd_based
			break
		fi
	done
	
	echo -n "[?] Now we need to create a virtual environment for python3 in $(pwd). Do you wish to proceed? (y/N): "
	read ANSWER
	ANSWER=$(to_lowercase "$ANSWER")
	if [[ "$ANSWER" == "y" ]]; then
		install_python_requirements
	else
		echo -e "${GREEN}[*] Success!${RESET}"
		exit 0
	fi
}

function check_privileges() {
	if [ "$(id -u)" -eq 0 ]; then
		main
	else
		echo -e "${RED}[!] Error: This script requires root privileges to install packages.${RESET}"
		exit 1
	fi
}

function parse_args() {
	if [[ $# -eq 0 ]]; then
		check_privileges
		return
	fi

	while [[ $# -gt 0 ]]; do
		case "$1" in
			-p|--packages)
				list_of_packages
				exit 0
				;;
			-i|--install)
				check_privileges
				;;
			*)
				echo -e "${RED}[!] Error: Unknown argument: $1 ${RESET}"
				exit 1
				;;
		esac
		shift
	done
}

parse_args "$@"
