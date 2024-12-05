#!/bin/bash

function check_privileges() {
	if [ "$(id -u)" -eq 0 ]; then
		main
	else
		echo "[!] Error: This script requires root privileges to install packages."
		exit 1
	fi
}

function check_tun() {
	if [ ! -e /dev/net/tun ]; then
		return 1
	fi

}

function main() {
	ARCH_BASED_DISTROS=("arch" "artix" "manjaro" "garuda" "hyperbola" "parabola" "endeavouros" "blackarch" "librewolfos")
	DEBIAN_BASED_DISTROS=("debian" "ubuntu" "xubuntu" "kubuntu" "mint" "lmde" "trisquel" "devuan" "kali" 
		"parrot" "pop" "elementary" "mx" "antix" "steamos" "tails" "astra" "crunchbag"
		"crunchbag++" "pureos" "deepin" "zorin" "peppermintos" "lubuntu" "wubuntu"
	)
	
	echo "+---- OpenVPN Setup ----+"
	echo -n "[==>] Enter the base of your GNU/Linux or BSD distribution: "
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
		fi
	done

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
}

check_privileges
check_tun
main
