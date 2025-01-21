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
#
# If you have the_unix_manager.sh located somewhere else - change this variable to the actual path:
# shellcheck source=/usr/bin/the_unix_manager.sh
declare TUM_PATH="/usr/bin/the_unix_manager.sh"
if [[ -f "$TUM_PATH" ]]; then
	if source "$TUM_PATH"; then
		echo -e "${GREEN}[*] Successfully imported theUnixManager. Loading global variables...${RESET}"

		declare DISTROS_COUNT="52"
		declare THE_SUFFOCATER_CONTRIBUTORS="3.5"
		declare THE_SUFFOCATER_VERSION_STRING=$(cat /etc/tsf/versions/tsf_version.txt)
		declare THE_CARCASS_VERSION_STRING=$(cat /etc/tsf/versions/tc_version.txt)

		echo -e "${GREEN}[*] Variables are successfully initialized. Loading main function...${RESET}"	
	else
		echo -e "${RED}[!] Error: the_unix_manager.sh not imported. Exiting... ${RESET}"
		exit 1
	fi
fi

function final_exit() {
	exit 0
}

function the_suffocater_help() {
	echo -e "\nCommands:"
	echo " exit - exit theSuffocater."
	echo " clear - clear the screen."
	echo " help - display this message."
	echo " neofetch - brief theSuffocater statistics."
	echo " import - for importing modules from directories."
	echo " scripts - list imported scripts."
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
	if [[ -f "/etc/tsf/markdown/LICENSE.md" ]]; then
		less /etc/tsf/markdown/LICENSE.md
	else
		echo -e "${RED}[!] Error: 'LICENSE.md' file not found. Broken installation?"
	fi
}

function the_suffocater_changelog() {
	if [[ -f "/etc/tsf/markdown/CHANGELOG.md" ]]; then
		less /etc/tsf/markdown/CHANGELOG.md
	else
		echo -e "${RED}[!] Error: 'CHANGELOG.md' file not found. Broken installation?"
	fi	
}

function the_suffocater_documentation {
	if [[ -f "/etc/tsf/markdown/README.md" ]]; then
		less /etc/tsf/markdown/README.md
	else
		echo -e "${RED}[!] Error: 'README.md' file not found. Broken installation?"
	fi
}

function the_suffocater_neofetch() {
	echo "${BLUE}               
	         __________           ${RESET}theSuffocater version - ${GREEN}$THE_SUFFOCATER_VERSION_STRING${BLUE}      
                [0000000000]          
            [0000000000000000.        
          [000000]         .  .       ${RESET}Adapted distributions count - ${GREEN}$DISTROS_COUNT${BLUE}
	  [00000]          [000]      ${RESET}Current contributors - ${GREEN}$THE_SUFFOCATER_VERSION_STRING${BLUE}
       [00000]             [000]      ${BLACK}███${WHITE}███${YELLOW}███${ORANGE}███${BLUE} 
       [00000]          [0000000000]  ${GREEN}███${RED}███${BLUE}███${PURPLE}███${BLUE}                      
       [0000]            ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺ 
        [00000.   ____  
         [0000.  .0000]          
            [0.  .000000.   __
             ⎺   .000000.  .00]        
                     [00.  .0000]    
      __________      ⎺⎺   [00000]    
     [0000000000]          [00000]       
        [000]              [00000]  
        [000]             [00000] 
         .  .           [000000]
          .0000000000000000]  
              [0000000]                              
               ⎺⎺⎺⎺⎺⎺⎺ ${RESET}"
}

function the_carcass_version() {
	echo "Current theCarcass version - $THE_CARCASS_VERSION_STRING"
}

function import_scripts() {
	echo "..."
}

function list_imported_scripts() {
	echo "..."
}

function the_carcass() {
        echo "+---------------- Welcome to theSuffocater ----------------+"
	echo " Current tSF version - $THE_SUFFOCATER_VERSION_STRING"
	echo " Current tC version - $THE_CARCASS_VERSION_STRING"
	echo "+----------------------------------------------------------+"
    
}

clear_screen
the_carcass
