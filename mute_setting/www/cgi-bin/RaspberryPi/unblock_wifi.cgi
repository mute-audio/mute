#!/bin/bash

# unblock_wifi.cgi              				 #
# (C)2023 kitamura_design <kitamura_design@me.com> #

# Initialize wpa_supplicant.conf

WPA_CONF="/etc/wpa_supplicant/wpa_supplicant.conf"

if [ ! -e $WPA_CONF ]; then
	sudo cp /var/www/cgi-bin/etc/wpa_supplicant.conf.bkup /etc/wpa_supplicant/wpa_supplicant.conf
fi

# Check current OS Codename
OS_codename=$(lsb_release -a | grep Codename | cut -f 2)

if [ ${OS_codename} = "buster" ] || [ ${OS_codename} = "bullseye" ]; then  # In case of Buster, Bullseye etc.

	sudo rfkill unblock wifi 2>/dev/null 1>/dev/null
	sudo systemctl restart dhcpcd.service 2>/dev/null 1>/dev/null

	sleep 5

	echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"           # Go back to the Page
	echo ""

else

    sudo nmcli radio wifi on 2>/dev/null 1>/dev/null

	sleep 5

    echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"			# Go back to the Page
    echo ''

fi

exit 0
