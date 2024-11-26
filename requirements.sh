#!/bin/bash

clear

list_of_platforms() {
	GUIX_BASED_DISTROS=("guix")
	REDHAT_BASED_DISTROS=("redhat")
	CENTOS_BASED_DISTROS=("centos")
	FEDORA_BASED_DISTROS=("fedora")
	DRAGORA_BASED_DISTROS=("dragora")
	OPENSUSE_BASED_DISTROS=("opensuse")
	SLACKWARE_BASED_DISTROS=("slackware")
	ALPINE_BASED_DISTROS=("alpine" "postmarket")
	VOID_BASED_DISTROS=("void" "argon" "shikake" "pristine")
	GENTOO_BASED_DISTROS=("gentoo" "funtoo" "calculate" "chromeos")
	OPENBSD_BASED_DISTROS=("openbsd" "adj" "libertybsd")
	NETBSD_BASED_DISTROS=("netbsd" "blackbsd" "edgebsd")
	FREEBSD_BASED_DISTROS=("freebsd" "ghostbsd" "midnightbsd" "bastillebsd" "cheribsd" "trueos" "dragonflybsd" "hardenedbsd" "hellosystem" "truenas")
	ARCH_BASED_DISTROS=("arch" "artix" "manjaro" "garuda" "hyperbola" "parabola" "endeavour" "blackarch" "librewolfos")
	DEBIAN_BASED_DISTROS=("debian" "ubuntu" "xubuntu" "kubuntu" "mint" "lmde" "trisquel" "devuan" "kali" 
		"parrot" "pop" "elementary" "mx" "antix" "steamos" "tails" "astra" "crunchbag"
		"crunchbag++" "pureos" "deepin" "zorin" "peppermintos" "lubuntu" "wubuntu"
	)
	
	echo "Supported Platforms:"
	for ELEMENT in "${GUIX_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${REDHAT_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${CENTOS_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${FEDORA_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${DRAGORA_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${OPENSUSE_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${SLACKWARE_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${ALPINE_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${VOID_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${GENTOO_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${OPENBSD_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${NETBSD_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${FREEBSD_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${ARCH_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
	
	for ELEMENT in "${DEBIAN_BASED_DISTROS[@]}"; do 
		echo " - $ELEMENT" 
	done
}

list_of_packages() {
	PACKAGES=("python3" "python3-pip"
		"net-tools" "ufw" "iptables" "nftables" "fail2ban"
		"openvpn" "wireguard/wireguard-tools"
		"git" "lsof"
	)

	echo "Packages to install:"
	for ELEMENT in "${PACKAGES[@]}"; do 
		echo " - $ELEMENT" 
	done
}

install_python_requirements() {
	python3 -m venv pkgenv
	source pkgenv/bin/activate
	pip install -r python_requirements.txt
		
	echo "Don't forget to 'source pkgenv/bin/activate' and you are good to go."
}

install_debian_based() {
	apt update && apt full-upgrade -y
	apt install python3 python3-pip -y
	apt install net-tools iproute2 ufw iptables fail2ban nftables -y
	apt install openvpn wireguard wireguard-tools -y
	apt install lsof git -y
}

install_arch_based() {
	pacman -Syu --noconfirm
	pacman -S python python-pip --noconfirm
	pacman -S net-tools iproute2 ufw iptables nftables fail2ban --noconfirm
	pacman -S openvpn wireguard-tools --noconfirm
	pacman -S lsof git --noconfirm
}

install_gentoo_based() {
	echo "Im sorry but you are on your own."
	echo "Install packages manually"
	exit 0
}

install_alpine_based() {
	apk update && apk upgrade
	apk add python3 py3-pip
	apk add net-tools iproute2 ufw iptables nftables fail2ban
	apk add wireguard-tools openvpn
	apk add lsof git
}

install_void_based() {
	xbps-install -Su
	xbps-install python3 python3-pip
	xbps-install net-tools iproute2 ufw iptables nftables fail2ban
	xbps-install openvpn wireguard-tools
	xbps-install lsof git
}

install_fedora_based() {
	dnf update -y
	dnf install python3 python3-pip -y
	dnf install net-tools iproute2 firewalld iptables-services nftables fail2ban -y
	dnf install openvpn wireguard-tools -y
	dnf install lsof git -y
}

install_opensuse_based() {
	zypper refresh && zypper update -y
	zypper install -y python3 python3-pip
	zypper install -y net-tools iproute2 firewalld iptables nftables fail2ban
	zypper install -y openvpn wireguard-tools
	zypper install -y lsof git
}

install_slackware_based() {
	echo "Im sorry but you are on your own."
	echo "Install packages manually."
}

install_redhat_based() {
	yum update -y && yum upgrade -y
	yum install python3 python3-pip -y
	yum install net-tools iproute2 firewalld iptables-services nftables fail2ban -y
	yum install openvpn wireguard-tools -y
	yum install lsof git -y
}

install_freebsd_based() {
	pkg update -y && pkg upgrade -y
	pkg install -y python3 py3-pip
	pkg install -y net-tools iproute2 iptables-legacy nftables fail2ban
	pkg intsall -y openvpn wireguard-tools
	pkg install -y lsof git
}

install_netbsd_based() {
	pkgin update -y && pkgin upgrade -y
	pkgin install python3 py3-pip 
	pkgin install nettools iproute2 iptables-legacy nftables fail2ban
	pkgin install lsof git
}

install_openbsd_based() {
	pkg_add -u
	pkg_add -uf
	pkg_add python3 py3-pip
	pkg_add nettools iproute2 pfctl fail2ban nftables
	pkg_add openvpn wireguard-tools
	pkg_add lsof git
}

install_dragora_based() {
	qi upgrade 
	qi install python3 python3-pip
	qi install net-tools iproute2 ufw iptables nftables fail2ban
	qi install openvpn wiregurard-tools
	qi install lsof git
}

to_lowercase() {
	echo "$1" | tr "[:upper:]" "[:lower:]"
}

main() {
	echo -n "[==>] Enter the base of your GNU/Linux or BSD distribution ('list' to view supported platforms, 'packges' to view requirements): "
	read DISTRO
	
	if [[ "$DISTRO" == "list" ]]; then
		list_of_platforms
		main
		return
	fi

	if [[ "$DISTRO" == "packages" ]]; then
		list_of_packages
		main
		return
	fi
	
	echo "--------------------------------------------------------------------------------------"
	echo "[<==] Installing requirements..."
	sleep 1

	DISTRO=$(to_lowercase "$DISTRO")
	case "$DISTRO" in
		*debian*|*ubuntu*|*xubuntu*|*mint*|*lmde*|*trisquel*|*devuan*|*kali*|*parrot*|*pop*|*elementary*|*mx*|*antix*)
			install_debian_based
			;;
		*arch*|*manjaro*|*garuda*|*hyperbola*|*parabola*|*artix*)
			install_arch_based
			;;
		*gentoo*)
			install_gentoo_based
			;;
		*alpine*)
			install_alpine_based
			;;
		*void*)
			install_void_based
			;;
		*fedora*)
			install_fedora_based
			;;
		*opensuse*)
			install_opensuse_based
			;;
		*slackware*)
			install_slackware_based
			;;
		*redhat*|*centos*)
			install_redhat_based
			;;
		*freebsd*|*ghostbsd*|*midnightbsd*)
			install_freebsd_based
			;;
		*netbsd*)
			install_netbsd_based
			;;
		*openbsd*)
			install_openbsd_based
			;;
		*dragora*)
			install_dragora_based
			;;
		*)
			echo "[!] Error: Unsupported distribution '$DISTRO'."
			exit 1
			;;
	esac
	
	sleep 1
	clear
	echo -n "[?] Now we need to create a virtual environment for python3 in $(pwd). Do you wish to proceed? (y/n): "
	read ANSWER
	
	ANSWER=$(to_lowercase "$ANSWER")
	
	if [[ "$ANSWER" == "y" ]]; then
		install_python_requirements
	else
		exit 0
	fi
}

check_privileges() {
	if [ "$(id -u)" -eq 0 ]; then
		main
	else
		echo "[!] Error: This script requires root privileges to install packages."
		exit 1
	fi
}

parse_args() {
	if [[ $# -eq 0 ]]; then
		check_privileges
		return
	fi

	while [[ $# -gt 0 ]]; do
		case "$1" in
			-l|--list)
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
				echo "[!] Error: Unknown argument: $1"
				exit 1
				;;
		esac
		shift
	done
}

parse_args "$@"
