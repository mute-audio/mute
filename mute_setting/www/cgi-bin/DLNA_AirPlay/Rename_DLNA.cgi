#!/bin/bash
# Rename_DLNA.cgi
# (C)2026 kitamura_design <kitamura_design@me.com>
# Collaborated with Gemini

# Extract Name from Query String
NEW_NAME=$(echo "$QUERY_STRING" | grep -o 'dlnaNAME=[^&]*' | cut -d'=' -f2)

if [ -n "$NEW_NAME" ]; then
    # 1. Replace '+' with space (Required for HTML form decoding)
    DECODED_STEP1="${NEW_NAME//+/ }"

    # 2. URL Decode %xx to actual characters (UTF-8)
    DECODED_NAME=$(echo -e "${DECODED_STEP1//%/\\x}")

    # 3. Apply to upmpdcli configuration
    sudo sed -i "s|^avfriendlyname =.*|avfriendlyname = $DECODED_NAME|" /etc/upmpdcli.conf

    # 4. Restart service
    sudo systemctl restart upmpdcli
fi

# Response for fetch
echo "Status: 200 OK"
echo "Content-type: text/plain"
echo ""
echo "done"