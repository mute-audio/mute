#!/bin/bash

# block_wifi.cgi		                         #
# (C)2023 kitamura_design <kitamura_design@me.com> #

# Check current OS Codename
OS_codename=$(lsb_release -a | grep Codename | cut -f 2)

if [ ${OS_codename} = "buster" ] || [ ${OS_codename} = "bullseye" ]; then  # In case of Buster, Bullseye etc.

    # Go back to the Page
    echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
    echo ""

    sudo rfkill block wifi 2>/dev/null 1>/dev/null

else

    sudo nmcli radio wifi off 2>/dev/null 1>/dev/null

    echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
    echo ''


fi

exit 0
