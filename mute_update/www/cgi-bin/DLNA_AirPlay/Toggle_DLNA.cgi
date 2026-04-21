#!/bin/bash
# Toggle_DLNA.cgi (Background Task)

# Check current status
CHK_STATUS=$(sudo systemctl is-enabled upmpdcli 2>/dev/null || echo "disabled")

if [ "$CHK_STATUS" = "enabled" ]; then
    sudo systemctl disable --now upmpdcli
else
    sudo systemctl enable --now upmpdcli
fi

echo "Status: 200 OK"
echo "Content-type: text/plain"
echo ""
echo "done"
