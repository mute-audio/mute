#!/bin/bash
# Toggle_DLNA.cgi (Background Task)
# (C)2026 kitamura_design <kitamura_design@me.com> #
# Collaborated with Gemini

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
