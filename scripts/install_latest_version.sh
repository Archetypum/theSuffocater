#!/bin/bash

clear

check_internet_connection() {
	echo "Checking internet connection..."
	if ping -c 1 "www.gnu.org" &>/dev/null; then
		echo "[*] Internet connection: OK"
	else
		echo "[*] Error: No internet connection detected."
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
	echo "[*] Installing latest theSuffocater version..."
	sleep 1
	
	git clone https://github.com/Kinderfeld/fear-thesuffocater
}

check_internet_connection
check_git_installed
install_latest_version
