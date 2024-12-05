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
	echo "+---- Wireguard Setup ----+"
	echo -n "[==>] Enter the base of your GNU/Linux or BSD distribution: "
	read DISTRO
}

check_privileges
check_tun
