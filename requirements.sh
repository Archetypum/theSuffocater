#!/bin/bash

clear

list_of_platforms() {
	DISTRIBUTIONS=("debian" "ubuntu" "mint" "lmde" "trisquel" "arch" "artix" "manjaro" "hyperbola" "parabola" "gentoo" "alpine" "void" "fedora" "opensuse" "slackware" "redhat" "freebsd" "netbsd" "openbsd" "dragora")
	for ELEMENT in "${DISTRIBUTIONS[@]}"; do
		echo "$ELEMENT"
	done
}

echo -n "Enter the base of your GNU+Linux or BSD distribution
(Or type 'list' to check the list of supported platforms): "

read DISTRO

if [[ "$DISTRO" == "list" ]]; then
	list_of_platforms
	exit 0
fi

echo "--------------------------------------------------------------"

DISTRO=$(echo "$DISTRO" | tr '[:upper:]' '[:lower:]')

install_debian_based() {
	apt update && apt upgrade -y
	apt install python3 python3-pip net-tools ufw iptables fail2ban openvpn nftables -y
}

install_arch_based() {
	pacman -Syu --noconfirm
	pacman -S python3 python3-pip net-tools ufw iptables fail2ban openvpn nftables --noconfirm
}

install_gentoo() {
	emerge --sync
	emerge -uDN @world
	emerge dev-python/pip
	echo "Gentoo setup is not fully implemented yet."
	echo "You are Gentoo user after all, install iptables, ufw, fail2ban, openvpn, nftables etc. yourself!"
}

install_alpine() {
	apk update && apk upgrade
	apk add python3 py3-pip net-tools ufw iptables fail2ban openvpn nftables
}

install_void() {
	xbps-install -S
	xbps-install python3 python3-pip net-tools ufw iptables fail2ban openvpn nftables
}

install_fedora() {
	dnf update -y
	dnf install python3 python3-pip net-tools firewalld fail2ban openvpn nftables -y
}

install_opensuse() {
	zypper refresh
	zypper install -y python3 python3-pip net-tools firewalld fail2ban openvpn nftables
}

install_slackware() {
	slackpkg update
	slackpkg install python3 python3-pip net-tools iptables fail2ban openvpn nftables
}

install_redhat() {
	yum update -y
	yum install python3 python3-pip net-tools firewalld fail2ban openvpn nftables -y
}

install_freebsd() {
	pkg update
	pkg install -y python3 py37-pip net-tools iptables fail2ban openvpn nftables
}

install_netbsd() {
	pkgin update
	pkgin install python37 py37-pip net-tools iptables fail2ban openvpn nftables
}

install_openbsd() {
	pkg_add python3 py3-pip net-tools pfctl fail2ban openvpn nftables
}

install_dragora() {
	pkg add python3 python3-pip net-tools ufw iptables fail2ban openvpn
}

case "$DISTRO" in
	*debian* | *ubuntu* | *mint* | *lmde* | *trisquel*)
		install_debian_based
		;;
	*arch* | *manjaro* | *hyperbola* | *parabola* | *artix*)
		install_arch_based
		;;
	*gentoo*)
		install_gentoo
		;;
	*alpine*)
		install_alpine
		;;
	*void*)
		install_void
		;;
	*fedora*)
		install_fedora
		;;
	*opensuse*)
		install_opensuse
		;;
	*slackware*)
		install_slackware
		;;
	*redhat*)
		install_redhat
		;;
	*freebsd*)
		install_freebsd
		;;
	*netbsd*)
		install_netbsd
		;;
	*openbsd*)
		install_openbsd
		;;
	*dragora*)
		install_dragora
		;;
	*)
		echo "Error: Unsupported distribution '$DISTRO'."
		exit 1
		;;
esac

echo "Don't forget to 'source pkgenv/bin/activate' and you're all set!"

