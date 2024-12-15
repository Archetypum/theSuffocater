#!/bin/bash

clear

# Fancy color codes ;3
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"

REDHAT_BASED_DISTROS=("redhat")
CENTOS_BASED_DISTROS=("centos" "oracle")
FEDORA_BASED_DISTROS=("fedora" "rocky" "mos")
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

FIRMWARE_PACKAGES="\

	atmel-firmware \
	bluez-firmware \
	dahdi-firmware-nonfree \
	firmware-amd-graphics \
	firmware-atheros \
	firmware-bnx2 \
	firmware-bnx2x \
	firmware-brcm80211 \
	firmware-cavium \
	firmware-intel-sound \
	firmware-iwlwifi \
	firmware-libertas \
	firmware-linux-free \
	firmware-linux-nonfree \
	firmware-misc-nonfree \
	firmware-myricom \
	firmware-netxen \
	firmware-qlogic \
	firmware-realtek \
	firmware-ti-connectivity \
	firmware-zd1211
"

function remove_redhat_based() {
	echo ""
}

function remove_fedora_based() {
	echo ""
}

function remove_opensuse_based() {
	echo ""
}

function remove_slackware_based() {
	echo ""
}

function remove_alpine_based() {
	echo ""
}

function remove_void_based() {
	echo ""
}

function remove_gentoo_based() {
	echo ""
}

function remove_arch_based() {
	echo ""
}

function remove_debian_based() {
	echo ""
}

function list_of_packages() {
	echo "Packages to install:"
	for ELEMENT in "${FIRMWARE_PACKAGES[@]}"; do 
		echo " - $ELEMENT" 
	done
}

function to_lowercase() {
	echo "$1" | tr "[:upper:]" "[:lower:]"
}

function main() {
	echo -n "[==>] Enter the base of your GNU/Linux distribution ('packages' to view requirements): "
	read DISTRO
	if [[ "$DISTRO" == "packages" ]]; then
		list_of_packages
		main
		return
	fi

	DISTRO=$(to_lowercase "$DISTRO")
	echo "[<==] Installing requirements..."
	echo "--------------------------------------------------------------------------------------"

	for ITEM in "${DEBIAN_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_debian_based
			break
		fi
	done
	
	for ITEM in "${ARCH_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_arch_based
			break
		fi
	done
	
	for ITEM in "${GUIX_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_guix_based
			break
		fi
	done
	
	for ITEM in "${REDHAT_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_redhat_based
			break
		fi
	done

	for ITEM in "${CENTOS_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_centos_based
			break
		fi
	done

	for ITEM in "${FEDORA_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_fedora_based
			break
		fi
	done

	for ITEM in "${DRAGORA_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_dragora_based
			break
		fi
	done

	for ITEM in "${OPENSUSE_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_opensuse_based
			break
		fi
	done

	for ITEM in "${SLACKWARE_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_slackware_based
			break
		fi
	done

	for ITEM in "${ALPINE_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_alpine_based
			break
		fi
	done

	for ITEM in "${VOID_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_void_based
			break
		fi
	done

	for ITEM in "${GENTOO_BASED_DISTROS[@]}"; do
		if [[ "$DISTRO" == "$ITEM" ]]; then
			remove_gentoo_based
			break
		fi
	done
}

function check_privileges() {
	if [ "$(id -u)" -eq 0 ]; then
		main
	else
		echo -e "${RED}[!] Error: This script requires root privileges to install packages.${RESET}"
		exit 1
	fi
}

function parse_args() {
	if [[ $# -eq 0 ]]; then
		check_privileges
		return
	fi

	while [[ $# -gt 0 ]]; do
		case "$1" in
			-p|--packages)
				list_of_packages
				exit 0
				;;
			-r|--remove)
				check_privileges
				;;
			*)
				echo -e "${RED}[!] Error: Unknown argument: $1 ${RESET}"
				exit 1
				;;
		esac
		shift
	done
}

parse_args "$@"
