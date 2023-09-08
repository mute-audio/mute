#!/bin/bash

# SSID_STS.cgi                              #
# (C)2023 kitamura_design <kitamura_design@me.com> #

ssid_STS=$(iwconfig wlan0 | grep "wlan0" | cut -d ":" -f 2 | cut -d "\"" -f 2)
ssid_LIST=$(sudo iwlist wlan0 scan | grep ESSID | sort | uniq | cut -d ":" -f 2 | cut -d "\"" -f 2 | sed -e 's/^/<option>/g' -e 's/$/<\/option>/g')

cat <<HTML
<select  id="ssid" name="ssid" class="inputbox">
<option selected>${ssid_STS:- ( No WiFi connection )}</option>
${ssid_LIST}
</select>
HTML

exit 0