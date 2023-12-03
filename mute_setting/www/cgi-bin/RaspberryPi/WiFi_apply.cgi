#!/bin/bash

# WiFi_apply.cgi		                         #
# (C)2023 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)
SSID=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | nkf -Ww --url-input)
PWD=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | nkf -Ww --url-input)

# Check current OS Codename
OS_codename=$(lsb_release -a |  grep Codename | cut -f 2)

if [ ${OS_codename} = "bookworm" ]; then  # In case of Bookworm

    sudo nmcli device wifi connect $SSID password $PWD 2>/dev/null 1>/dev/null

    #### Rewrite /etc/wpa_supplicant/wpa_supplicant.conf
    sudo sed -i -e "/ssid/s/\".*\"/\"$SSID\"/g" -e "/psk/s/\".*\"/\"$PWD\"/g" /etc/wpa_supplicant/wpa_supplicant.conf

    echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi?$query"
    echo ''

else  # In case of Buster, Bullseye etc.

    #### Rewrite /etc/wpa_supplicant/wpa_supplicant.conf
    sudo sed -i -e "/ssid/s/\".*\"/\"$SSID\"/g" -e "/psk/s/\".*\"/\"$PWD\"/g" /etc/wpa_supplicant/wpa_supplicant.conf

    sudo systemctl restart dhcpcd.service

    #### Force-Reload /etc/wpa_supplicant/wpa_supplicant.conf
    sudo wpa_cli -i wlan0 reconfigure >  /dev/null

    sleep 4

    echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi?$query"
    echo ''

fi

exit 0
