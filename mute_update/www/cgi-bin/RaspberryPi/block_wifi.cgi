#!/bin/bash

# block_wifi.cgi		                         #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Go back to the Page
echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
echo ""

set -e

sudo rfkill block wifi
#wait

