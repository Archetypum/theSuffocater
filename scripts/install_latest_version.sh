#!/bin/bash

source /usr/bin/the_unix_manager.sh

function check_internet_connection() {
	echo "Checking internet connection..."
	if ping -c 1 "www.gnu.org" &>/dev/null; then
		echo -e "${GREEN}[*] Internet connection: OK.${RESET}"
	else
		echo -e "${RED}[!] Error: No internet connection detected.${RESET}"
		exit 1
	fi
}

function check_git_installed() {
	if ! command -v git &>/dev/null; then
		echo -e "${RED}[!] Error: Git is not installed.${RESET}"
		exit 1
	fi
}

function install_latest_version() {
	git pull origin main && echo -e "${GREEN}[*] Success!${RESET}"
}

function install_latest_version_new_dir() {
	if [ $# -eq 0 ]; then
		echo -e "${RED}[!] WARNING:"
		echo "    You are going to install new theSuffocater version to the root directory."
		echo -e "    To prevent this, run this script directly without the carcass and without root privileges.${RESET}"
		echo -n "[?] Wish to proceed and install to the root? (y/N): "
		read ANSWER
		if [ "$ANSWER" == "y" ]; then
			echo "[<==] Installing latest theSuffocater version..."
			sleep 1
			
			git clone https://github.com/Archetym/thesuffocater thesuffocater-new && echo -e "${GREEN}[*] Success!${RESET}"
		fi
	fi
}

check_internet_connection
check_git_installed

echo -n "[?] Install new version in new directory or just replace old files? (New/Replace): "
read ANSWER
if [[ "$ANSWER" == "n" ]]; then
	install_latest_version_new_dir
elif [[ "$ANSWER" == "r" ]]; then
	install_latest_version

fi
