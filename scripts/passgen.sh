#!/bin/bash
# ---------------------------------------
# Simple password generator that uses random symbols + random word from the dictionary.
# GNU/Linux, BSD, Windows, OS X supported.
# 
# Author: iva
# Date: 28.07.2024
# ---------------------------------------

source /usr/bin/the_unix_manager.sh

function passgen() {
	echo -ne "We are going to create a strong password.\n"
	if prompt_user "[?] Proceed?"; then
		read -p "[==>] Enter password name: " NAME
		read -p "[==>] Enter password length: " PASSWORD_LENGTH
		
		if ! [[ "$PASSWORD_LENGTH" =~ ^[0-9]+$ ]]; then
			echo -e "${RED}[!] Error: Password length must be a number.${RESET}"
			exit 1
		fi
		
		
		local CHARACTERS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-=_+"
		local RANDOM_CHARS=""
		for I in $(seq 1 $PASSWORD_LENGTH); do
			local RANDOM_CHARS+=$(echo -n "$CHARACTERS" | fold -w1 | shuf | head -n1)
		done
		
		local CREATED_PASSWORD="$RANDOM_CHARS"
		
		echo "$NAME $CREATED_PASSWORD" > "$NAME.txt"
		echo -e "[*] Your new password for $NAME: $CREATED_PASSWORD"
		echo -e "[<==] Saving to $NAME.txt..."
		echo -e "${GREEN}[*] Success!${RESET}"
	fi
}

passgen
