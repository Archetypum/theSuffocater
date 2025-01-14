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
ARCH_BASED_DISTROS=("arch" "artix" "manjaro" "garuda" "hyperbola" "parabola" "endeavouros" "blackarch" "librewolfos")
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
	
	echo "[<==] Creating /etc/wireguard/ and generating keys..."
	sleep 1
	mkdir /etc/wireguard >/dev/null 2>&1
	chmod 600 -R /etc/wireguard/
	
	echo "[<==] Generating keys..."
	sleep 1
	SERVER_PRIVATE_KEY=$(wg genkey)
	SERVER_PUBLIC_KEY=$(echo "${SERVER_PRIVATE_KEY}" | wg pubkey)

	echo "SERVER_PUB_IP=${SERVER_PUB_IP}
SERVER_PUB_NIC=${SERVER_PUB_NIC}
SERVER_WG_NIC=${SERVER_WG_NIC}
SERVER_WG_IPV4=${SERVER_WG_IPV4}
SERVER_WG_IPV6=${SERVER_WG_IPV6}
SERVER_PORT=${SERVER_PORT}
SERVER_PRIVATE_KEY=${SERVER_PRIVATE_KEY}
SERVER_PUBLIC_KEY=${SERVER_PUBLIC_KEY}
CLIENT_DNS_1=${CLIENT_DNS_1}
CLIENT_DNS_2=${CLIENT_DNS_2}
ALLOWED_IPS=${ALLOWED_IPS}" > /etc/wireguard/params
	
	echo "[Interface]
Address = ${SERVER_WG_IPV4}/24,${SERVER_WG_IPV6}/64
ListenPort = ${SERVER_PORT}
PrivateKey = ${SERVER_PRIVATE_KEY}" > "/etc/wireguard/${SERVER_WG_NIC}.conf"
	
	echo "[<==] Setting up firewall rules..."
	sleep 1
	echo "PostUp = iptables -I INPUT -p udp --dport ${SERVER_PORT} -j ACCEPT
PostUp = iptables -I FORWARD -i ${SERVER_PUB_NIC} -o ${SERVER_WG_NIC} -j ACCEPT
PostUp = iptables -I FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostUp = iptables -t nat -A POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE
PostUp = ip6tables -I FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostUp = ip6tables -t nat -A POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE
PostDown = iptables -D INPUT -p udp --dport ${SERVER_PORT} -j ACCEPT
PostDown = iptables -D FORWARD -i ${SERVER_PUB_NIC} -o ${SERVER_WG_NIC} -j ACCEPT
PostDown = iptables -D FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE
PostDown = ip6tables -D FORWARD -i ${SERVER_WG_NIC} -j ACCEPT
PostDown = ip6tables -t nat -D POSTROUTING -o ${SERVER_PUB_NIC} -j MASQUERADE" >> "/etc/wireguard/${SERVER_WG_NIC}.conf"
	echo "net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1" > /etc/sysctl.d/wg.conf
	
	sysctl --system

	echo -n "[==>] Enter your init systemm: "
	read INIT_SYSTEM
	if [[ "$INIT_SYSTEM" == "sysvinit" ]]; then
		service "wg-quick@${SERVER_WG_NIC}" start
	elif [[ "$INIT_SYSTEM" == "systemd" ]]; then
		systemctl start "wg-quick@${SERVER_WG_NIC}"
		systemctl enable "wg-quick@${SERVER_WG_NIC}"
	else
		echo -e "${RED}[!] Error: Unsupported init system '${INIT_SYSTEM}'${RESET}"
	fi
}

function remove_debian_based() {
	echo "[<==] Removing Wireguard..."
	sleep 1

	apt update
	apt upgrade -y
	apt purge wireguard wireguard-tools qrencode -y
}

function install_arch_based() {
	echo "[<==] Installing Wireguard..."
	sleep 1

	pacman -Syu
	pacman -S wireguard-tools qrencode --noconfirm 
}

function remove_alpine_based() {
	echo "[<==] Removing Wireguard..."
	sleep 1

	apk update && apk upgrade
	apk del wireguard-tools qrencode
}

get_home() {
	CLIENT=$1
	if [[ -z "${CLIENT}" ]]; then
		echo -e "${RED}[!] Error: No client name specified.${RESET}"
		exit 1
	fi

	if [[ -e "/home/${CLIENT}" ]]; then
		HOME_DIRECTORY="/home/${CLIENT}"
	else
		HOME_DIRECTORY="/root"
	fi

	echo "$HOME_DIRECTORY"
}

function make_client() {
	if [[ ${SERVER_PUBLIC_IP} =~ .*:.* && ${SERVER_PUBLIC_IP} != *"["* && ${SERVER_PUBLIC_IP} != *"]"* ]]; then
		SERVER_PUBLIC_IP="[${SERVER_PUBLIC_IP}]"
	fi

	ENDPOINT="${SERVER_PUBLIC_IP}:${SERVER_PORT}"

	until [[ ${CLIENT_NAME} =~ ^[a-zA-Z0-9_-]+$ && ${CLIENT_EXISTS} == "0" && ${#CLIENT_NAME} -lt 16 ]]; do
		echo -n "[==>] New client name: "
		read CLIENT_NAME
		CLIENT_EXISTS=$(grep -c -E "^### Client ${CLIENT_NAME}$" "/etc/wireguard/${SERVER_WG_NIC}.conf")
		[[ ${CLIENT_EXISTS} != 0 ]] && echo -e "${RED}[!] Error: Client with the specified name already exists.${RESET}"
	done

	for DOT_IP in {2..254}; do
		DOT_EXISTS=$(grep -c "${SERVER_WG_IPV4::-1}${DOT_IP}" "/etc/wireguard/${SERVER_WG_NIC}.conf")
		[[ "${DOT_EXISTS}" == "0" ]] && break
	done

	[[ "${DOT_EXISTS}" == "1" ]] && { echo -e "${RED}[!] Error: The subnet supports only 253 clients.${RESET}"; exit 1; }

	BASE_IP=$(echo "$SERVER_WG_IPV4" | awk -F "." '{ print $1"."$2"."$3 }')

	until [[ ${IPV4_EXISTS} == "0" ]]; do
		read -rp "[==>] Client WireGuard IPv4: ${BASE_IP}." -e -i "${DOT_IP}" DOT_IP
		CLIENT_WG_IPV4="${BASE_IP}.${DOT_IP}"
		IPV4_EXISTS=$(grep -c "$CLIENT_WG_IPV4/32" "/etc/wireguard/${SERVER_WG_NIC}.conf")
		[[ ${IPV4_EXISTS} != 0 ]] && echo -e "${RED}[!] Error: Client with the specified IPv4 already exists.${RESET}"
	done

	BASE_IP=$(echo "$SERVER_WG_IPV6" | awk -F "::" "{ print $1 }")

	until [[ ${IPV6_EXISTS} == "0" ]]; do
		read -rp "[==>] Client WireGuard IPv6: ${BASE_IP}::" -e -i "${DOT_IP}" DOT_IP
		CLIENT_WG_IPV6="${BASE_IP}::${DOT_IP}"
		IPV6_EXISTS=$(grep -c "${CLIENT_WG_IPV6}/128" "/etc/wireguard/${SERVER_WG_NIC}.conf")
		if [[ ${IPV6_EXISTS} != 0 ]]; then
			echo -e "${RED}[!] Error: Client with the specified IPv6 already exists.${RESET}"
		fi
	done

	CLIENT_PRIVATE_KEY=$(wg genkey)
	CLIENT_PUBLIC_KEY=$(echo "${CLIENT_PRIVATE_KEY}" | wg pubkey)
	CLIENT_PRE_SHARED_KEY=$(wg genpsk)

	HOME_DIRECTORY=$(get_home "${CLIENT_NAME}")

	echo "[Interface]
PrivateKey = ${CLIENT_PRIVATE_KEY}
Address = ${CLIENT_WG_IPV4}/32,${CLIENT_WG_IPV6}/128
DNS = ${CLIENT_DNS_1},${CLIENT_DNS_2}

[Peer]
PublicKey = ${SERVER_PUBLIC_KEY}
PresharedKey = ${CLIENT_PRE_SHARED_KEY}
Endpoint = ${ENDPOINT}
AllowedIPs = ${ALLOWED_IPS}" > "${HOME_DIRECTORY}/${SERVER_WG_NIC}-client-${CLIENT_NAME}.conf"

	echo -e "### Client ${CLIENT_NAME}
[Peer]
PublicKey = ${CLIENT_PUBLIC_KEY}
PresharedKey = ${CLIENT_PRE_SHARED_KEY}
AllowedIPs = ${CLIENT_WG_IPV4}/32,${CLIENT_WG_IPV6}/128" >> "/etc/wireguard/${SERVER_WG_NIC}.conf"

	TMPFILE=$(mktemp)
	wg-quick strip "${SERVER_WG_NIC}" > "$TMPFILE"
	wg syncconf "${SERVER_WG_NIC}" < "$TMPFILE"
	rm -f "$TMPFILE"

	if command -v qrencode &>/dev/null; then
		echo -e "${GREEN}[*] Client QR Code:${RESET}"
		qrencode -t ansiutf8 -l L <"${HOME_DIRECTORY}/${SERVER_WG_NIC}-client-${CLIENT_NAME}.conf"
	fi

	echo -e "${GREEN}[*] Config file location:${HOME_DIRECTORY}/${SERVER_WG_NIC}-client-${CLIENT_NAME}.conf${RESET}"
	echo -e "${GREEN}[*] Success!"
}

function remove_client() {
	echo -n "[==>] Enter client to remove: "
	
	read CLIENT
	sed -i "/^### Client ${CLIENT}\$/,/^$/d" "/etc/wireguard/${SERVER_WG_NIC}.conf"
	HOME=$(get_home "${CLIENT}")
	rm -f "${HOME}/${SERVER_WG_NIC}-client-${CLIENT}.conf"
	wg syncconf "${SERVER_WG_NIC}" <(wg-quick strip "${SERVER_WG_NIC}")
	echo -e "${GREEN}[*] Success!${RESET}"
}

function list_clients() {
	CLIENTS_COUNT=$(grep -c -E "^### Client" "/etc/wireguard/${SERVER_WG_NIC}.conf")
	if [[ ${CLIENTS_COUNT} -eq 0 ]]; then
		echo "You don't have any clients yet."
	fi

	grep -E "^### Client" "/etc/wireguard/${SERVER_WG_NIC}.conf" | cut -d " " -f 3 | nl -s ") "
}

function install_questions() {
	clear

	echo "..."
}

function install_wireguard() {
	install_questions
	clear

	echo "+---- Wireguard Setup ----+"
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

function remove_wireguard() {
	clear

	echo -e "${RED}[!] WARNING: This will uninstall WireGuard and remove all the configuration files!"
	echo -e "Please backup the /etc/wireguard directory if you want to keep your configuration files.${RESET}"
	echo -n "Proceed? (y/N): "
	read REMOVE
	
	REMOVE=$(echo "$REMOVE" | tr "[:upper:]" "[:lower:]")	
	if [[ "$REMOVE" == "y" ]]; then
		echo -n "[==>] Enter the base of your GNU/Linux or BSD distribution: "
		read DISTRO
		
		DISTRO=$(echo "$DISTRO" | tr "[:upper:]" "[:lower:]")
		for ITEM in "${DEBIAN_BASED_DISTROS[@]}"; do
			if [[ "$DISTRO" == "$ITEM" ]]; then
				remove_debian_based
				rm -rf /etc/wireguard
				rm -f /etc/sysctl.d/wg.conf && echo -e "${GREEN}[*] Success!${RESET}"
			fi
		done
		
		for ITEM in "${ARCH_BASED_DISTROS[@]}"; do
			if [[ "$DISTRO" == "$ITEM" ]]; then
				remove_arch_based
				rm -rf /etc/wireguard
				rm -f /etc/sysctl.d/wg.conf && echo -e "${GREEN}[*] Success!${RESET}"
			fi
		done
	fi
}

function menu() {
	clear

	echo "+---- Ultimate Wireguard ----+"
	echo "  - add_users"
	echo "  - list_users"
	echo "  - remove_users"
	echo "  - remove_wireguard"
	echo "  - exit"
	echo -n "[==>] Enter function: "
	read FUNCTION
	case "${FUNCTION}" in
		add_users)
			make_client
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
		remove_wireguard)
			remove_wireguard
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
			-I|--install-wireguard)
				install_wireguard
				exit 0
				;;
			-R|--remove-wireguard)
				remove_wireguard
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

if [[ -e /etc/wireguard/params ]]; then
	source /etc/wireguard/params
	menu
else
	install_wireguard
fi

parse_args "$@"
