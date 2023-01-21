#!/bin/bash

# WiFi_apply.cgi		                         #
# (C)2022 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)
SSID=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | nkf -Ww --url-input)
PWD=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | nkf -Ww --url-input)

#### Rewrite /etc/wpa_supplicant/wpa_supplicant.conf
sudo sed -i -e "/ssid/s/\".*\"/\"$SSID\"/g" -e "/psk/s/\".*\"/\"$PWD\"/g" /etc/wpa_supplicant/wpa_supplicant.conf

sudo systemctl restart dhcpcd.service

#### Force-Reload /etc/wpa_supplicant/wpa_supplicant.conf
sudo wpa_cli -i wlan0 reconfigure >  /dev/null

sleep 4

echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi?$query"
echo ''
