#!/bin/bash

# unblock_wifi.cgi              				 #
# (C)2022 kitamura_design <kitamura_design@me.com> #

WPA_CONF="/etc/wpa_supplicant/wpa_supplicant.conf"

if [ ! -e $WPA_CONF ]; then
	sudo cp /var/www/cgi-bin/etc/wpa_supplicant.conf.bkup /etc/wpa_supplicant/wpa_supplicant.conf
fi

sudo rfkill unblock wifi 2>/dev/null 1>/dev/null

sudo systemctl restart dhcpcd.service 2>/dev/null 1>/dev/null

sleep 5

echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"           # Go back to the Page
echo ""
