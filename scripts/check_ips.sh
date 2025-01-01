#!/bin/bash

WHITE_LIST="white_list.txt"
LOG_FILE="vpn_connection_check.log"

if [[ ! -f "$WHITE_LIST" ]]; then
    echo "white_list.txt not found at $WHITE_LIST" | tee -a "$LOG_FILE"
    exit 1
fi

if [[ ! -f "$LOG_FILE" ]]; then
	echo "vpn_connection_check.log not found at $LOG_FILE"
	exit 1
fi

echo "----- Script Started: $(date) -----" | tee -a "$LOG_FILE"
ACTIVE_CONNECTIONS=$(netstat -tn | grep -E ':[0-9]{5}' | awk '{print $5}' | cut -d':' -f1 | sort | uniq)
if [ -z "$ACTIVE_CONNECTIONS" ]; then
	echo "No active connections found." | tee -a "$LOG_FILE"
else
	echo "Checking active connections against white list..." | tee -a "$LOG_FILE"
	for IP in $ACTIVE_CONNECTIONS; do
		if grep -qw "$IP" "$WHITE_LIST"; then
			echo "Allowed connection: $IP" | tee -a "$LOG_FILE"
		else
			echo "Suspicious connection: $IP (not in white list)" | tee -a "$LOG_FILE"
		fi
	done
fi

echo "----- Script Ended: $(date) -----" | tee -a "$LOG_FILE"

