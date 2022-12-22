#!/bin/bash

# Country_Select.cgi                             #
# (C)2022 kitamura_design <kitamura_design@me.com> #

#### Rewrite /etc/wpa_supplicant/wpa_supplicant.conf
 current=$(sudo cat /etc/wpa_supplicant/wpa_supplicant.conf | grep country)
 COUNTRY=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | nkf -Ww --url-input)

 sudo sed -i -e s/$current/$COUNTRY/g /etc/wpa_supplicant/wpa_supplicant.conf

## Go back to page
 echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
 echo ""
