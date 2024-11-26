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

remove_old_thesuffocater() {
	echo -n "[?] Remove old theSuffocater related files? (y/N): "
	read ANSWER
	if [ "$ANSWER" == "y" ]; then
		# rm -rf .git
		rm -rf pkgenv
		rm -rf modules
		rm -rf scripts
		rm -rf config_files
		rm -r requirements.sh
		rm -r the_suffocater_cli.py
		rm -r the_suffocater_gui.py
		rm -r python_requirements.txt
		rm -r README.md
		rm -r LICENSE.md
		rm -r CHANGELOG.md 
		echo "Success!"
		exit 0
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
			
			git clone https://github.com/Kinderfeld/fear-thesuffocater fear-the-suffocater-new && echo "Success!"
		fi

		remove_old_thesuffocater
}

check_internet_connection
check_git_installed
install_latest_version
