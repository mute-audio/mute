#!/bin/bash

# Rename_AirPlay.cgi
# (C)2026 kitamura_design <kitamura_design@me.com>

# Extract Name from Query String
NEW_NAME=$(echo "$QUERY_STRING" | grep -o 'airplayNAME=[^&]*' | cut -d'=' -f2)

if [ -n "$NEW_NAME" ]; then
    # 1. Replace '+' with space
    DECODED_STEP1="${NEW_NAME//+/ }"

    # 2. URL Decode %xx to UTF-8
    DECODED_NAME=$(echo -e "${DECODED_STEP1//%/\\x}")

    # 3. Rewrite only the line starting with "name =" (ignoring mixer_control_name)
    # Using sed with a regex for line start and optional spaces
    sudo sed -i "s/^[[:space:]]*name = \".*\";/    name = \"$DECODED_NAME\";/" /etc/shairport-sync.conf

    # Restart AirPlay service (No daemon-reload needed for .conf files)
    sudo systemctl restart shairport-sync
fi

echo "Status: 200 OK"
echo "Content-type: text/plain"
echo ""
echo "done"
