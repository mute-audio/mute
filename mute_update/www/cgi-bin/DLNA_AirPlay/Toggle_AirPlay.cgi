#!/bin/bash
# Toggle_AirPlay.cgi (Background Task)

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
