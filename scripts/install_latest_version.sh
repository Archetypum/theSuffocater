#!/bin/bash

check_internet_connection() {
	echo "Checking internet connection..."
	if ping -c 1 "www.gnu.org" &>/dev/null; then
		echo "[*] Internet connection: OK."
	else
		echo "[!] Error: No internet connection detected."
		exit 1
	fi
	}

check_git_installed() {
	if ! command -v git &>/dev/null; then
		echo "[!] Error: Git is not installed."
		exit 1
	fi
}

install_latest_version() {
	if [ $# -eq 0 ]; then
		echo "[!] WARNING:"
		echo "    You are going to install new theSuffocater version to the root directory."
		echo "    To prevent this, run this script directly without the carcass and without root privileges."
		echo -n "[?] Wish to proceed and install to the root? (y/N): "
		read ANSWER
	fi
		if [ "$ANSWER" == "y" ]; then
			echo "[<==] Installing latest theSuffocater version..."
			sleep 1
			
			git clone https://github.com/Kinderfeld/fear-thesuffocater fear-the-suffocater-new && echo "Success"
		fi
}

# check_internet_connection
check_git_installed
install_latest_version
