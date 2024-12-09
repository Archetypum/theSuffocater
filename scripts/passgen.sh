#!/bin/bash

# Fancy color codes ;3
RED="\033[0;31m"
GREEN="\033[0;32m"
RESET="\033[0m"

function passgen() {
	echo -n "We are going to create a strong password."
	read -p "[?] Proceed? (y/N): " ANSWER
	
	ANSWER=$(echo "$ANSWER" | tr "[:upper:]" "[:lower:]")
	if [[ "$ANSWER" == "y" || "$ANSWER" == "yes" ]]; then
		read -p "[==>] Enter password name: " NAME
		read -p "[==>] Enter password length: " PASSWORD_LENGTH
		
		if ! [[ "$PASSWORD_LENGTH" =~ ^[0-9]+$ ]]; then
			echo -e "${RED}[!] Error: Password length must be a number.${RESET}"
			exit 1
		fi
		
		
		CHARACTERS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-=_+"
		RANDOM_CHARS=""
		for I in $(seq 1 $PASSWORD_LENGTH); do
			RANDOM_CHARS+=$(echo -n "$CHARACTERS" | fold -w1 | shuf | head -n1)
		done
		
		CREATED_PASSWORD="$RANDOM_CHARS"
		
		echo "$NAME $CREATED_PASSWORD" > "$NAME.txt"
		echo -e "[*] Your new password for $NAME: $CREATED_PASSWORD"
		echo -e "[<==] Saving to $NAME.txt..."
		echo -e "${GREEN}[*] Success!${RESET}"
	fi
}

passgen
