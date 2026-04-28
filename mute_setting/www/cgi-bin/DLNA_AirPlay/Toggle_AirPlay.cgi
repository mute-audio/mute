#!/bin/bash
# Toggle_AirPlay.cgi (Background Task)
# (C)2026 kitamura_design <kitamura_design@me.com> #
# Collaborated with Gemini

# Check current status
CHK_STATUS=$(sudo systemctl is-enabled shairport-sync 2>/dev/null || echo "disabled")

if [ "$CHK_STATUS" = "enabled" ]; then
    sudo systemctl disable --now shairport-sync
else
    sudo systemctl enable --now shairport-sync
fi

echo "Status: 200 OK"
echo "Content-type: text/plain"
echo ""
echo "done"
