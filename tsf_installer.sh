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

	read -rp "[==>] " OPTION
	if [[ "$OPTION" == "1" ]]; then
		install_thesuffocater
	elif [[ "$OPTION" == "2" ]]; then
		remove_thesuffocater
	else
		echo -e "${RED} Invalid option: $OPTION${RESET}"
		return 1
	fi
}

function list_of_commands() {
	# Helping ourselves.
	
	echo "Help page:"
	echo " -h/--help - lists commands."
	echo " -i/--install - Installs theSuffocater to your system."
	echo " -r/--remove - Removes theSuffocater from your system."
	echo " -d/--debug - Debugging mode for developers."
}

function install_thesuffocater() {
	# Moves install/src/the_carcass_cli.py, the_carcass_gui.py to /usr/bin
	# Moves install/tsf to /etc/tsf
	# Creates markdown/ directory at /etc/tsf and moves all .md files to /etc/tsf/markdown
	# Creates aliases in ~/.bashrc and ~/.zshrc
	
	check_privileges

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

	if [[ -f "$HOME/.bashrc" ]]; then
		echo -e "${GREEN}[<==] Creating aliases in ~/.bashrc...${RESET}"
		echo "alias thesuffocater_cli='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_cli.py\"'" >> ~/.bashrc
		echo "alias thesuffocater_gui='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_gui.py\"'" >> ~/.bashrc
	fi

	if [[ -f "$HOME/.zshrc" ]]; then
		echo -e "${GREEN}[<==] Creating aliases in ~/.zshrc${RESET}"
		echo "alias thesuffocater_cli='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_cli.py\"'" >> ~/.zshrc
		echo "alias thesuffocater_gui='bash -c \"source ~/.pkgenv/bin/activate && python3 /usr/bin/the_carcass_gui.py\"'" >> ~/.zshrc
	fi

	echo -e "${GREEN}[*] Success!${RESET}"
	return 0
}

function remove_thesuffocater() {
	# Purges all tSF files from the /etc/, ~, and /usr/bin
	
	check_privileges

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
	#
	# On Alpine Linux needs 'util-linux' package installed.
	
	echo -e "${PURPLE}CLI theCarcass:${RESET}"
	whereis the_carcass_cli.py  # Should be /usr/bin/the_carcass_cli.py
	echo -e "${PURPLE}GUI theCarcass:${RESET}"
	whereis the_carcass_gui.py  # Should be /usr/bin/the_carcass_gui.py
	echo -e "${PURPLE}tSF configs:${RESET}"
	whereis tsf  # Should be /etc/tsf
	echo -e "${PURPLE}TheUnixManager-bash:${RESET}"
	whereis the_unix_manager.sh
}

function clone_unstable_repository() {
	# Clones theSuffocater-unstable via git.
	#
	# Requires git. Huh.
	
	echo -e "${GREEN}\n[==>] Cloning repository...\n${RESET}"
	git clone https://github.com/Archetypum/theSuffocater theSuffocater-unstable && echo -e "${GREEN}\n[*] Success!${RESET}"
}

function parse_args() {
	if [[ $# -eq 0 ]]; then
		main
		return
	fi

	while [[ $# -gt 0 ]]; do
		case "$1" in
			"-h"|"--help")
				list_of_commands
				exit 0
				;;
			"-i"|"--install")
				install_thesuffocater
				exit 0
				;;
			"-r"|"--remove")
				remove_thesuffocater
				exit 0
				;;
			"-d"|"--debug")
				debug
				exit 0
				;;
			"-c"|"--clone")
				clone_unstable_repository
				exit 0
				;;
			*)
				echo -e "${RED}[!] Error: Unknown argument: $1${RESET}"
				exit 1
				;;
		esac
	done
}

parse_args "$@"
