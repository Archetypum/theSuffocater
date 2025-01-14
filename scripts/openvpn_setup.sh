#!/bin/bash

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

function install_debian_based() {
	echo "..."
}

function install_arch_based() {
	echo "..."
}

function unbound_remove() {
	clear

	echo "..."
}

function unbound_setup() {
	clear

	echo "+---- OpenVPN Setup ----+"
	echo -n "[==>] Enter the base of your GNU/Linux distribution: "
	read DISTRO
	
	for ITEM in "${DEBIAN_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			echo "interface: 10.8.0.1
access-control: 10.8.0.1/24 allow
hide-identity: yes
hide-version: yes
use-caps-for-id: yes
prefetch: yes" >> /etc/unbound/unbound.conf	
		fi
	done
	
	for ITEM in "${ARCH_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			curl -o /etc/unbound/root.hints https://www.internic.net/domain/named.cache
			
			if [[ ! -f /etc/unbound/unbound.conf.old ]]; then
				mv /etc/unbound/unbound.conf /etc/unbound/unbound.conf.old
			fi
		echo "server:
		use-syslog: yes
		do-daemonize: no
		username: "unbound"
		directory: "/etc/unbound"
		trust-anchor-file: trusted-key.key
		root-hints: root.hints
		interface: 10.8.0.1
		access-control: 10.8.0.1/24 allow
		port: 53
		num-threads: 2
		use-caps-for-id: yes
		harden-glue: yes
		hide-identity: yes
		hide-version: yes
		qname-minimisation: yes
		prefetch: yes" > /etc/unbound/unbound.conf
		fi
	done

	if [[ $IPV6_SUPPORT == "y" ]]; then
		echo "interface: fd42:42:42:42::1
access-control: fd42:42:42:42::/112 allow" >> /etc/unbound/unbound.conf
		
		echo "private-address: 10.0.0.0/8
private-address: fd42:42:42:42::/112
private-address: 172.16.0.0/12
private-address: 192.168.0.0/16
private-address: 169.254.0.0/16
private-address: fd00::/8
private-address: fe80::/10
private-address: 127.0.0.0/8
private-address: ::ffff:0:0/96" >> /etc/unbound/unbound.conf
	fi

}

function make_client() {
	echo "..."
}

function remove_client() {
	echo "..."
}

function list_clients() {
	echo "..."
}

function install_questions() {
	clear

	echo "..."
}

function install_openvpn() {
	install_questions
	clear

	echo "+---- OpenVPN Setup ----+"
	echo -n "[==>] Enter the base of your GNU/Linux distribution: "
	read DISTRO

	DISTRO=$(echo "$DISTRO" | tr "[:upper:]" "[:lower:]")
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
}

function remove_openvpn() {
	clear

	echo "..."
}

function menu() {
	clear

	echo "+---- Ultimate OpenVPN ----+"
	echo "  - add_users"
	echo "  - list_users"
	echo "  - remove_users"
	echo "  - remove_openvpn"
	echo "  - exit"
	echo -n "[==>] Enter function: "
	read FUNCTION
	case "${FUNCTION}" in
		add_users)
			new_client
			exit 0
			;;
		list_users)
			list_clients
			exit 0
			;;
		remove_users)
			remove_client
			exit 0
			;;
		remove_openvpn)
			remove_openvpn
			exit 0
			;;
		exit)
			exit 0
			;;
		@)
			echo -e "${RED}[!] Error: Invalid input.${RESET}"
			;;
	esac
}

function parse_args() {
	if [[ $# -eq 0 ]]; then
		check_privileges
		menu
		return
	fi

	while [[ $# -gt 0 ]]; do
		case "$1" in
			-m|--make-client)
				make_client
				exit 0
				;;
			-r|--remove-client)
				remove_client
				exit 0
				;;
			-l|--list-clients)
				list_clients
				exit 0
				;;
			-I|--install-openvpn)
				install_openvpn
				exit 0
				;;
			-R|--remove-openvpn)
				remove_openvpn
				exit 0
				;;
			*)
				echo -e "${RED}[!] Error: Unknown argument: $1 ${RESET}"
				exit 1
				;;
		esac
		shift
	done
}

function check_privileges() {
	if [[ "$(id -u)" -eq 0 ]]; then
		menu
	else
		echo -e "${RED}[!] Error: This script requires root privileges to install packages.${RESET}"
		exit 1
	fi
}

function check_tun() {
	if [[ ! -e /dev/net/tun ]]; then
		return 1
	fi

}

if [[ -e /etc/openvpn/server.conf ]]; then
	menu
else
	install_openvpn
fi

parse_args "$@"
