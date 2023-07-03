#!/bin/bash

# block_wifi.cgi		                         #
# (C)2023 kitamura_design <kitamura_design@me.com> #

# Go back to the Page
echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
echo ""

sudo rfkill block wifi 2>/dev/null 1>/dev/null
