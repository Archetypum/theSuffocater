#!/bin/bash
#
# If you have the_unix_manager.sh located somewhere else - change this variable to the actual path:
#
# shellcheck source=/usr/bin/the_unix_manager.sh
declare TUM_PATH="/usr/bin/the_unix_manager.sh"
source "$TUM_PATH"

function remove_thesuffocater() {
	if prompt_user "[?] Are you sure you want to remove theSuffocater from your system?"; then
		rm -rf ~/.pkgenv && echo -e "${GREEN}\n[<==] Removing python venv...${RESET}"
		rm -rf /etc/tsf && echo -e "${GREEN}[<==] Purging configuration files...${RESET}"
		rm -f /usr/bin/the_carcass_cli && echo -e "${GREEN}[<==] Removing theCarcass CLI executable...${RESET}"
		rm -f /usr/bin/the_carcass_gui && echo -e "${GREEN}[<==] Removing theCarcass GUI executable...${RESET}"
		rm -rf /usr/bin/_internal && echo -e "${GREEN}[<==] Removing dependencies for executables...\n"
	else
		exit 0
	fi
}

check_privileges
remove_thesuffocater
