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
	# Main function
	#
	# Provides functions to install or remove tSF.
	# Planning to add update && upgrade functionality later.
	
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
	# Moves install/src/the_carcass_cli.py, the_carcass_gui.py to /usr/bin
	# Moves install/tsf to /etc/tsf
	# Creates markdown/ directory at /etc/tsf and moves all .md files to /etc/tsf/markdown
	# Creates aliases in ~/.bashrc and ~/.zshrc
	
	if [[ -f "install/src/the_carcass_cli.py" ]]; then
		cp install/src/the_carcass_cli.py /usr/bin/the_carcass_cli.py && echo -e "${GREEN}[==>] Moving theCarcassCLI to /usr/bin...${RESET}"
	fi

	if [[ -f "install/src/the_carcass_gui.py" ]]; then
		cp install/src/the_carcass_gui.py /usr/bin/the_carcass_gui.py && echo -e "${GREEN}[==>] Moving theCarcassGUI to /usr/bin...${RESET}"
	fi
	
	if [[ -d "install/tsf" ]]; then
		cp -r  install/tsf /etc/tsf && echo -e "${GREEN}[==>] Moving configurations directory to /etc/tsf...${RESET}"
		mkdir /etc/tsf/markdown
		cp CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md LICENSE-GPL.md LICENSE-MIT.md PULL_REQUEST_TEMPLATE.md README.md SECURITY.md /etc/tsf/markdown
	fi

	if [[ -f "~/.bashrc" ]]; then
		echo -e "${GREEN}[<==] Creating aliases in ~/.bashrc...${RESET}"
		echo "alias thesuffocater_cli='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_cli.py\"'" >> ~/.bashrc
		echo "alias thesuffocater_gui='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_gui.py\"'" >> ~/.bashrc
	fi

	if [[ -f "~/.zshrc" ]]; then
		echo -e "${GREEN}[<==] Creating aliases in ~/.zshrc${RESET}"
		echo "alias thesuffocater_cli='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_cli.py\"'" >> ~/.zshrc
		echo "alias thesuffocater_gui='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_gui.py\"'" >> ~/.zshrc
	fi

	echo -e "${GREEN}[*] Success!${RESET}"
	return 0
}

function remove_thesuffocater() {
	# Purges all tSF files from the /etc/, ~, and /usr/bin
	if prompt_user "[?] Are you sure you want to remove theSuffocater from your system?"; then
		rm -rf ~/.pkgenv && echo -e "${GREEN}\n[<==] Removing python venv...${RESET}"
		rm -rf /etc/tsf && echo -e "${GREEN}[<==] Purging configuration files...${RESET}"
		rm -f /usr/bin/the_carcass_cli.py && echo -e "${GREEN}[<==] Removing theCarcass CLI from /usr/bin...${RESET}"
		rm -f /usr/bin/the_carcass_gui.py && echo -e "${GREEN}[<==] Removing theCarcass GUI from /usr/bin...${RESET}"
		echo -e "\n${GREEN}[*] Successfully removed theSuffocater from your system.${RESET}"
		echo -e "${GREEN}[*] Don't forget to remove aliases from ~/.bashrc and ~/.zshrc${RESET}"
	else
		return 0
	fi
}

function debug() {
	# Debugging function for checking where theSuffocater main components are located.
	# Sometimes can be very helpful, especially when you trying to port tSF on new distros
	# On Alpine Linux neeeds 'util-linux' package installed.
	
	echo -e "${PURPLE}CLI theCarcass:${RESET}"
	whereis the_carcass_cli.py  # Should be /usr/bin/the_carcass_cli.py
	echo -e "${PURPLE}GUI theCarcass:${RESET}"
	whereis the_carcass_gui.py  # Should be /usr/bin/the_carcass_gui.py
	echo -e "${PURPLE}tSF configs:${RESET}"
	whereis tsf  # Should be /etc/tsf
	echo -e "${PURPLE}TheUnixManager-bash:${RESET}"
	whereis the_unix_manager.sh
}

# debug
main
