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

	echo "SERVER_PUB_IP=${SERVER_PUB_IP}
SERVER_PUB_NIC=${SERVER_PUB_NIC}
SERVER_WG_NIC=${SERVER_WG_NIC}
SERVER_WG_IPV4=${SERVER_WG_IPV4}
SERVER_WG_IPV6=${SERVER_WG_IPV6}
SERVER_PORT=${SERVER_PORT}
SERVER_PRIV_KEY=${SERVER_PRIV_KEY}
SERVER_PUB_KEY=${SERVER_PUB_KEY}
CLIENT_DNS_1=${CLIENT_DNS_1}
CLIENT_DNS_2=${CLIENT_DNS_2}
ALLOWED_IPS=${ALLOWED_IPS}" > /etc/wireguard/params

	echo "[Interface]
Address = ${SERVER_WG_IPV4}/24,${SERVER_WG_IPV6}/64
ListenPort = ${SERVER_PORT}
PrivateKey = ${SERVER_PRIV_KEY}" >"/etc/wireguard/${SERVER_WG_NIC}.conf"
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

function remove_wireguard() {
	echo -n "[?] Are you sure you want to remove Wireguard? (y/N): "
	read ANSWER
	if [[ "$ANSWER" == "y" ]]; then
		apt purge wireguard wireguard-tools qrencode -y && echo "[*] Success!"
		rm -rf /etc/wireguard
		rm -f /etc/sysctl.d/wg.conf
	fi
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

function menu() {
	echo "+---- Ultimate Wireguard ----+"
}

function parse_args() {
	if [[ $# -eq 0 ]]; then
		check_privileges
		check_virt
		main
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
			-I|--install-wireguard)
				main
				exit 0
				;;
			-R|--remove-wireguard)
				remove_wireguard
				exit 0
				;;
			*)
				echo "[!] Error: Unknown argument: $1"
				exit 1
				;;
		esac
		shift
	done
}

if [[ -e /etc/wireguard/params ]]; then
	source /etc/wireguard/params
	menu
else
	main
fi


parse_args "$@"
