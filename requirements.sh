#!/bin/bash

clear

list_of_platforms() {
	DISTRIBUTIONS=(
		"void" "alpine" "gentoo" "dragora" "slackware"
		"fedora" "opensuse" "redhat"
		"freebsd" "netbsd" "openbsd"
		"arch" "artix" "manjaro" "hyperbola" "parabola"
		"debian" "ubuntu" "xubuntu" "mint" "lmde" "trisquel" "devuan" "kali" "parrot" "pop" "elementary"
	)
	
	echo "Supported Platforms:"
	for ELEMENT in "${DISTRIBUTIONS[@]}"; do
		echo " - $ELEMENT"
	done
}

list_of_packages() {
	PACKAGES=(
		"python3" "python3-pip"
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
	echo "Installing requirements..."
	sleep 1
	
	apt update && apt full-upgrade -y
	apt install python3 python3-pip -y
	apt install net-tools ufw iptables fail2ban nftables -y
	apt install openvpn wireguard wireguard-tools -y
	apt install lsof git -y
}

install_arch_based() {
	echo "Installing requirements..."
	sleep 1

	pacman -Syu --noconfirm
	pacman -S python python-pip --noconfirm
	pacman -S net-tools ufw iptables nftables fail2ban --noconfirm
	pacman -s openvpn wireguard-tools --noconfirm
	pacman -S lsof git --noconfirm
}

install_gentoo_based() {
	echo "Installing requirements..."
	sleep 1

	emerge --sync
	emerge -uDN @world
	
	echo "Gentoo setup is not fully implemented yet. Install it yourself, you are gentoo user after all!"
}

install_alpine_based() {
	echo "Installing requirements..."
	sleep 1

	apk update && apk upgrade
	apk add python3 py3-pip
	apk add net-tools ufw iptables nftables fail2ban
	apk add wireguard-tools openvpn
	apk add lsof git
}

install_void_based() {
	echo "Installing requirements..."
	sleep 1

	xbps-install -Su
	xbps-install python3 python3-pip
	xbps-install net-tools ufw iptables nftables fail2ban
	xbps-install openvpn wireguard-tools
	xbps-install lsof git
}

install_fedora_based() {
	echo "Installing requirements..."
	sleep 1
	
	dnf update -y && dnf upgrade -y
	dnf install python3 python3-pip -y
	dnf install net-tools firewalld iptables-services nftables fail2ban -y
	dnf install openvpn wireguard-tools -y
	dnf install lsof git -y
}

install_opensuse_based() {
	echo "Installing requirements..."
	sleep 1
	
	zypper refresh -y && zypper update -y
	zypper install -y python3 python3-pip
	zypper install -y net-tools firewalld iptables nftables fail2ban
	zypper install -y openvpn wireguard-tools
	zypper install -y lsof git
}

install_slackware_based() {
	echo "Installing requirements..."
	sleep 1

	echo "Im sorry but you are on your own."
	echo "Install packages manually from 'packages'."
}

install_redhat_based() {
	echo "Installing requirements..."
	sleep 1

	yum update -y && yum upgrade -y
	yum install python3 python3-pip -y
	yum install net-tools firewalld iptables-services nftables fail2ban -y
	yum install openvpn wireguard-tools -y
	yum install lsof git -y
}

install_freebsd_based() {
	echo "Installing requirements..."
	sleep 1

	pkg update -y && pkg upgrade -y
	pkg install -y python3 py3-pip
	pkg install -y net-tools iptables-legacy nftables fail2ban
	pkg intsall -y openvpn wireguard-tools
	pkg install -y lsof git
}

install_netbsd_based() {
	echo "Installing requirements..."
	sleep 1

	pkgin update -y && pkgin upgrade -y
	pkgin install python3 py3-pip 
	pkgin install nettools iptables-legacy nftables fail2ban
	pkgin install lsof git
}

install_openbsd_based() {
	echo "Installing requirements..."
	sleep 1
	
	pkg_add -u
	pkg_add -uf
	pkg_add python3 py3-pip
	pkg_add nettools pfctl fail2ban nftables
	pkg_add openvpn wireguard-tools
	pkg_add lsof git
}

install_dragora_based() {
	echo "Installing requirements..."
	sleep 1

	qi upgrade 
	qi install python3 python3-pip
	qi install net-tools ufw iptables nftables fail2ban
	qi install openvpn wiregurard-tools
	qi install lsof git
}

to_lowercase() {
	echo "$1" | tr "[:upper:]" "[:lower:]"
}

main() {
	echo -n "Enter the base of your GNU/Linux or BSD distribution ('list' to view supported platforms, 'packges' to view requirements): "
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
	
	DISTRO=$(to_lowercase "$DISTRO")
	
	case "$DISTRO" in
		*debian*|*ubuntu*|*xubuntu*|*mint*|*lmde*|*trisquel*|*devuan*|*kali*|*parrot*|*pop*|*elementary*)
			install_debian_based
			;;
		*arch*|*manjaro*|*hyperbola*|*parabola*|*artix*)
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
		*redhat*)
			install_redhat_based
			;;
		*freebsd*)
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
			echo "Error: Unsupported distribution '$DISTRO'."
			exit 1
			;;
	esac
	
	sleep 1
	clear
	echo -n "Now we need to create a virtual environment for Python3 in $(pwd). Do you wish to proceed? (y/n): "
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
		echo "This script requires root privileges to install packages."
		exit 1
	fi
}

check_privileges
