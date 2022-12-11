#!/bin/bash

# block_wifi.cgi		                         #
# ©2022 kitamura_design <kitamura_design@me.com> #

echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"           # Go back to the Page
echo ""

set -e

sudo rfkill block wifi
#wait

