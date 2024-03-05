#!/bin/bash

# SSID_STS.cgi                              #
# (C)2024 kitamura_design <kitamura_design@me.com> #

# Check current OS Codename
OS_codename=$(lsb_release -a |  grep Codename | cut -f 2)

if [ ${OS_codename} = "buster" ] || [ ${OS_codename} = "bullseye" ]; then  # In case of Buster, Bullseye etc.

    ssid_STS=$(iwconfig wlan0 | grep "wlan0" | cut -d ":" -f 2 | cut -d "\"" -f 2)
    ssid_LIST=$(sudo iwlist wlan0 scan | grep ESSID | sort | uniq | cut -d ":" -f 2 | cut -d "\"" -f 2 | sed -e 's/^/<option>/g' -e 's/$/<\/option>/g')
else

    ssid_STS=$(iwconfig wlan0 | grep "wlan0" | cut -d ":" -f 2 | cut -d "\"" -f 2)
    ssid_LIST=$(sudo nmcli -f SSID device wifi list | sed -e '/SSID/d' | sort | uniq | sed -e 's/^/<option>/g' -e 's/$/<\/option>/g')
fi


cat <<HTML
<select  id="ssid" name="ssid" class="inputbox-single">
<option selected>${ssid_STS:- ( No WiFi connection )}</option>
${ssid_LIST}
</select>
HTML

exit 0