#!/bin/bash

clear

list_of_platforms() {
	DISTRIBUTIONS=(
		"void" "alpine" "gentoo" "dragora" "slackware"
		"fedora" "opensuse" "redhat"
		"freebsd" "netbsd" "openbsd"
		"arch" "artix" "manjaro" "hyperbola" "parabola"
		"debian" "ubuntu" "mint" "lmde" "trisquel" "devuan" "kali" "parrot" "pop" "elementary"
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
		"openvpn" "wireguard"  "wireguard-tools"
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
	apt install python3 python3-pip
	apt install net-tools ufw iptables fail2ban nftables lsof git -y
	apt install openvpn wireguard wireguard-tools
}

install_arch_based() {
	echo "Installing requirements..."
	sleep 1

	pacman -Syu --noconfirm
	pacman -S python3 python3-pip --noconfirm
	pacman -S net-tools ufw iptables fail2ban nftables lsof git --noconfirm
	pacman -s openvpn wireguard wireguard-tools --noconfirm
}

install_gentoo_based() {
	echo "Installing requirements..."
	sleep 1

	emerge --sync
	emerge -uDN @world
	emerge dev-python/pip
	
	echo "Gentoo setup is not fully implemented yet. Install it yourself, you are gentoo user after all!"
}

install_alpine_based() {
	echo "Installing requirements..."
	sleep 1

	apk update && apk upgrade
	apk add python3 py3-pip
	apk add net-tools ufw iptables fail2ban nftables lsof git
	apt add wireguard wireguard-tools
}

install_void_based() {
	echo "Installing requirements..."
	sleep 1

	xbps-install -Su
	xbps-install python3 python3-pip
	xbps-install net-tools ufw iptables fail2ban openvpn nftables lsof git
}

install_fedora_based() {
	echo "Installing requirements..."
	sleep 1
	
	dnf update -y
	dnf install python3 python3-pip net-tools firewalld fail2ban openvpn nftables lsof git -y
}

install_opensuse_based() {
	echo "Installing requirements..."
	sleep 1
	
	zypper refresh
	zypper install -y python3 python3-pip
	zypper install -y net-tools firewalld fail2ban openvpn nftables lsof git
}

install_slackware_based() {
	echo "Installing requirements..."
	sleep 1

	slackpkg update
	slackpkg install python3 python3-pip
	slackpkg install net-tools iptables fail2ban openvpn nftables lsof git
}

install_redhat_based() {
	echo "Installing requirements..."
	sleep 1

	yum update -y
	yum install python3 python3-pip -y
	yum install net-tools firewalld fail2ban openvpn nftables lsof git -y
}

install_freebsd_based() {
	echo "Installing requirements..."
	sleep 1

	pkg update -y
	pkg install -y python3 py37-pip
	pkg install -y net-tools iptables fail2ban openvpn nftables lsof git
}

install_netbsd_based() {
	echo "Installing requirements..."
	sleep 1

	pkgin update
	pkgin install python37 py37-pip
	pkgin install net-tools iptables fail2ban openvpn nftables lsof git
}

install_openbsd_based() {
	echo "Installing requirements..."
	sleep 1

	pkg_add python3 py3-pip
	pkg_add net-tools pfctl fail2ban openvpn nftables lsof git
}

install_dragora_based() {
	echo "Installing requirements..."
	sleep 1

	pkg add python3 python3-pip
	pkg add net-tools ufw iptables fail2ban openvpn lsof git
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
		*debian*|*ubuntu*|*mint*|*lmde*|*trisquel*|*devuan*|*kali*|*parrot*|*pop*|*elementary*)
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
