#!/bin/bash
#
# If you have the_unix_manager.sh located somewhere else - change this variable to the actual path:
#
# shellcheck source=/usr/bin/the_unix_manager.sh
declare TUM_PATH="/usr/bin/the_unix_manager.sh"
source "$TUM_PATH"

function to_lowercase() {
	echo "$1" | tr "[:upper:]" "[:lower:]"
}

function list_of_commands() {
	echo "Help page:"
	echo " -h/--help - lists commands."
	echo " -p/--packages - lists packages to install."
	echo " -s/--systems - lists supported platforms."
}

function list_of_platforms() {	
	echo "Supported Platforms:"
	for ELEMENT in "${GUIX_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${REDHAT_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${CENTOS_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${FEDORA_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${DRAGORA_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${OPENSUSE_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${SLACKWARE_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${ALPINE_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${VOID_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${GENTOO_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${OPENBSD_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${NETBSD_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${FREEBSD_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${ARCH_BASED[@]}"; do echo " - $ELEMENT"; done 
	for ELEMENT in "${DEBIAN_BASED[@]}"; do echo " - $ELEMENT"; done
}

function list_of_packages() {
	local PACKAGES=("python3" "python3-pip"
		"net-tools" "ufw" "iptables" "nftables" "fail2ban"
		"openvpn" "wireguard/wireguard-tools"
		"git" "wget" "lsof" "bash" "unbound"
	)

	echo "Packages to install:"
	for ELEMENT in "${PACKAGES[@]}"; do 
		echo " - $ELEMENT" 
	done
}

function install_debian_based() {
	apt update && apt full-upgrade -y
	apt install python3 python3-pip python3.11-venv -y
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
	pkg install -y python3 python
	pkg install -y py311-fail2ban
	pkg install -y openvpn wireguard-tools
	pkg install -y lsof git wget bash curl unbound shuf 

	echo -e "${RED}[!] Warning:"
	echo "    Iptables, nftables, Iproute, and ufw are GNU/Linux specific tools."
	echo "    To achieve similar functionality, use tools designed for BSD systems,"
	echo -e "    like PF (Packet Filter), IPFilter (ipf), or build these packages yourself.${RESET}"
	echo -n "[==>] Hit enter to proceed: "
	read -r PROCEED
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
	read -r PROCEED
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
	read -r PROCEED
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

function compiling() {
	bash -c "source ~/.pkgenv/bin/activate && python3 compile.py"
}

function main() {
	read -rp "[==>] Enter your OS (GNU/Linux, BSD distro): " DISTRO
	DISTRO=$(to_lowercase "$DISTRO")
	if [[ "$DISTRO" == "packages" ]]; then
		list_of_packages
		main
		return
	elif [[ "$DISTRO" == "platforms" ]]; then
		list_of_platforms
		main
		return
	elif [[ "$DISTRO" == "help" ]]; then
		list_of_commands
		main
		return
	fi

	echo "[<==] Installing requirements..."
	echo "--------------------------------"

	for ITEM in "${DEBIAN_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_debian_based
			break
		fi
	done

	for ITEM in "${ARCH_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_arch_based
			break
		fi
	done

	for ITEM in "${GUIX_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_guix_based
			break
		fi
	done

	for ITEM in "${CENTOS_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_centos_based
			break
		fi
	done

	for ITEM in "${FEDORA_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_fedora_based
			break
		fi
	done

	for ITEM in "${DRAGORA_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_dragora_based
			break
		fi
	done

	for ITEM in "${OPENSUSE_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_opensuse_based
			break
		fi
	done

	for ITEM in "${SLACKWARE_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_slackware_based
			break
		fi
	done

	for ITEM in "${ALPINE_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_alpine_based
			break
		fi
	done

	for ITEM in "${VOID_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_void_based
			break
		fi
	done

	for ITEM in "${GENTOO_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_gentoo_based
			break
		fi
	done

	for ITEM in "${OPENBSD_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_openbsd_based
			break
		fi
	done

	for ITEM in "${NETBSD_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_netbsd_based
			install_python_requirements_netbsd
			compiling
			exit 0
		fi
	done

	for ITEM in "${FREEBSD_BASED[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_freebsd_based
			break
		fi
	done

	echo -e "\nNow we need to create a virtual environment for python3 in your home directory."
	echo -e "\nType in your terminal:"
	echo "    python3 -m venv ~/.pkgenv"
	echo "    source ~/.pkgenv/bin/activate"
	echo "    pip install -r install/python_requirements.txt"
	echo -e "\nAfter that, launch:"
	echo "    python3 compile.py"
}

function parse_args() {
	if [[ $# -eq 0 ]]; then
		clear
		check_privileges
		main
		return
	fi

	while [[ $# -gt 0 ]]; do
		case "$1" in
			-h|--help)
				list_of_commands
				exit 0
				;;
			-s|--systems)
				list_of_platforms
				exit 0
				;;
			-p|--packages)
				list_of_packages
				exit 0
				;;
			-i|--install)
				check_privileges
				;;
			*)
				echo -e "${RED}[!] Error: Unknown argument: $1${RESET}"
				exit 1
				;;
		esac
		shift
	done
}

parse_args "$@"
