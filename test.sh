#!/bin/bash

DEBIAN_BASED_DISTROS=("debian" "devuan" "mx")
DISTRO="devuan"

install_debian_based() {
	apt update && apt full-upgrade -y
	apt install python3 python3-pip -y
	apt install net-tools iproute2 ufw iptables fail2ban nftables -y
	apt install openvpn wireguard wireguard-tools -y
	apt install lsof git wget -y
}

main() {
	for ITEM in "${DEBIAN_BASED_DISTROS[@]}"; do
		echo $ITEM
		if [[ "$DISTRO" == "$ITEM" ]]; then
			install_debian_based
			break
		fi
	done
}

main
