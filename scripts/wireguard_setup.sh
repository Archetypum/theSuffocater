#!/bin/bash

DEBIAN_BASED_DISTROS=("debian" "ubuntu" "xubuntu" "kubuntu" "mint" "lmde" "trisquel" "devuan" "kali" 
	"parrot" "pop" "elementary" "mx" "antix" "steamos" "tails" "astra" "crunchbag"
	"crunchbag++" "pureos" "deepin" "zorin" "peppermintos" "lubuntu" "wubuntu"
)

function install_debian_based() {
	echo "[<==] Installing requirements..."
	sleep 1
	apt update
	apt upgrade -y
	apt install wireguard wireguard-tools iptables resolvconf qrencode
	
	echo "[<==] Creatinf /etc/wireguard/ and generating keys..."
	sleep 1
	mkdir /etc/wireguard >/dev/null 2>&1
	chmod 600 -R /etc/wireguard/

	SERVER_PRIVATE_KEY=$(wg genkey)
	SERVER_PUBLIC_KEY=$(echo "${SERVER_PRIV_KEY}" | wg pubkey)
}

function check_privileges() {
	if [ "$(id -u)" -eq 0 ]; then
		main
	else
		echo "[!] Error: This script requires root privileges to install packages."
		exit 1
	fi
}


function check_virt() {
	if [[ "$(systemd-detect-virt)" == "openvz" ]]; then
		echo "[!] Error: OpenVZ is not supported."
		exit 1
	fi
}

function main() {
	echo "+---- Wireguard Setup ----+"
	echo -n "[==>] Enter the base of your GNU/Linux or BSD distribution: "
	read DISTRO
	
	DISTRO=$(echo "$DISTRO" | tr "[:upper:]" "[:lower:]")
	for ITEM in "${DEBIAN_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_debian_based
			break
		fi
	done
}

check_privileges
chech_virt
main
