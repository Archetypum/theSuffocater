#!/bin/bash
#
# If you have the_unix_manager.sh located somewhere else - change this variable to the actual path:
#
# shellcheck source=/usr/bin/the_unix_manager.sh
declare TUM_PATH="/usr/bin/the_unix_manager.sh"
if [[ ! -f "$TUM_PATH" ]]; then
	echo "[!] Error: the_unix_manager.sh not found at $TUM_PATH. Please provide the correct path."
	exit 1
fi

source "$TUM_PATH"

function main() {
	clear

	local OPTION

	echo "+------ Welcome to theSuffocater installer ------+"
	echo -e "\nOptions:"
	echo "    1 - Install theSuffocater."
	echo -e "    2 - Remove theSuffocater.\n"

	read -p "[==>] " OPTION
	if [[ "$OPTION" == "1" ]]; then
		check_privileges
		install_thesuffocater
	elif [[ "$OPTION" == "2" ]]; then
		check_privileges
		remove_thesuffocater
	else
		echo -e "${RED} Invalid option: "$OPTION"${RESET}"
		return 1
	fi
}

function install_thesuffocater() {
	if [[ -f "install/src/the_carcass_cli.py" ]]; then
		cp install/src/the_carcass_cli.py /usr/bin/the_carcass_cli.py && echo -e "${GREEN}[==>] Moving theCarcassCLI to /usr/bin...${RESET}"
	fi

	if [[ -f "install/src/the_carcass_gui.py" ]]; then
		cp install/src/the_carcass_gui.py /usr/bin/the_carcass_gui.py && echo -e "${GREEN}[==>] Moving theCarcassGUI to /usr/bin...${RESET}"
	fi
	
	if [[ -d "install/tsf" ]]; then
		cp -r  install/tsf /etc/tsf && echo -e "${GREEN}[==>] Moving configurations directory to /etc/tsf...${RESET}"
	fi

	echo "alias thesuffocater_cli='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_cli.py\"'" >> ~/.bashrc
	echo "alias thesuffocater_gui='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_gui.py\"'" >> ~/.bashrc


	echo -e "${GREEN}[*] Success!${RESET}"
	return 0
}

function remove_thesuffocater() {
	if prompt_user "[?] Are you sure you want to remove theSuffocater from your system?"; then
		rm -rf ~/.pkgenv && echo -e "${GREEN}\n[<==] Removing python venv...${RESET}"
		rm -rf /etc/tsf && echo -e "${GREEN}[<==] Purging configuration files...${RESET}"
		rm -f /usr/bin/the_carcass_cli.py && echo -e "${GREEN}[<==] Removing theCarcass CLI from /usr/bin...${RESET}"
		rm -f /usr/bin/the_carcass_gui.py && echo -e "${GREEN}[<==] Removing theCarcass GUI from /usr/bin...${RESET}"
		echo -e "\n${GREEN}[*] Successfully removed theSuffocater from your system.${RESET}"
	else
		return 0
	fi
}

function debug() {
	# Debugging function for checking where theSuffocater main components are located.
	# Sometimes can be very helpful, especially when you trying to port tSF on new distros
	
	echo -e "${PURPLE}CLI theCarcass:${RESET}"
	whereis the_carcass_cli.py  # Should be /usr/bin/the_carcass_cli.py
	echo -e "${PURPLE}GUI theCarcass:${RESET}"
	whereis the_carcass_gui.py  # Should be /usr/bin/the_carcass_gui.py
	echo -e "${PURPLE}tSF configs:${RESET}"
	whereis tsf  # Should be /etc/tsf
	echo -e "${PURPLE}TheUnixManager-bash:${RESET}"
	whereis the_unix_manager.sh
}

debug
# main
