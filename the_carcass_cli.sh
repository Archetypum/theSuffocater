#!/bin/bash
#
# This thing is called "theCarcass" - heart of theSuffocater.
# theCarcass destiny is to load modules and scripts from directories provided by the user.
# for further using.
#
# Usually theCarcass don't receive many updates because it's already serving
# its functionality very good, but not in current release! Say hello to new theCarcass-2.0!
#
# Graphical frontend - the_carcass_gui.py
# Python version - the_carcass_cli.py

function final_exit() {
	exit 0
}

function the_suffocater_help() {
	echo -e "\nCommands:"
	echo " exit - exit theSuffocater."
	echo " clear - clear the screen."
	echo " help - display this message."
	echo " neofetch - brief theSuffocater statistics."
	echo " modules [-d] - list imported modules (use -d to include documentation)."
	echo " tsf_version - get current version of theSuffocater."
	echo " tc_version - get current version of theCarcass."
	echo " license - check license.md"
	echo " documentation - check readme.md"
	echo " changelog - check whats new in your current version"
	echo -e "\nFor more info, check 'documentation'."
}

function the_suffocater_version() {
	echo "Current theSuffocater version - $THE_SUFFOCATER_VERSION_STRING"
}

function the_suffocater_license() {
	if [[ -f "LICENSE.md" ]]; then
		less LICENSE.md
	else
		echo -e "${RED}[!] Error: 'LICENSE.md' file not found. Broken installation?"
	fi
}

function the_suffocater_changelog() {
	if [[ -f "CHANGELOG.md" ]]; then
		less CHANGELOG.md
	else
		echo -e "${RED}[!] Error: 'CHANGELOG.md' file not found. Broken installation?"
	fi	
}

function the_suffocater_documentation {
	if [[ -f "README.md" ]]; then
		less README.md
	else
		echo -e "${RED}[!] Error: 'README.md' file not found. Broken installation?"
	fi
}

function the_suffocater_neofetch() {
	echo "..."
}

function the_carcass_version() {
	echo "Current theCarcass version - $THE_CARCASS_VERSION_STRING"
}

function import_modules() {
	echo "..."
}

function list_imported_modules() {
	echo "..."
}

function the_carcass() {
	echo "..."
}

# If you have the_unix_manager.sh located somewhere else - change this variable to the actual path:
declare TUM_PATH="/usr/bin/the_unix_manager.sh"
if [[ -f "$TUM_PATH" ]]; then
	if source "$TUM_PATH"; then
		echo -e "${GREEN}[*] Successfully imported modules. Loading global variables...${RESET}"

		declare DISTROS="52"
		declare THE_SUFFOCATER_CONTRIBUTORS="3.5"
		declare THE_SUFFOCATER_VERSION_STRING=$(cat tsf_version.txt)
		declare THE_CARCASS_VERSION_STRING=$(cat tc_version.txt)

		echo -e "${GREEN}[*] Variables are successfully initialized. Loading main function...${RESET}"
		clear_screen
		the_carcass THE_SUFFOCATER_VERSION_STRING, THE_CARCASS_VERSION_STRING
	else
		echo -e "${RED}[!] Error: the_unix_manager.sh not imported. Exiting... ${RESET}"
		exit 1
	fi
fi
