#!/bin/bash

# Country_Select.cgi                             #
# (C)2025 kitamura_design <kitamura_design@me.com> #

# Extract Country Code From QueryString
COUNTRY=$(echo ${QUERY_STRING} | nkf -Ww --url-input)


# Check current OS Codename
OS_codename=$(lsb_release -a | grep Codename | cut -f 2)

# In case of Legacy OS
if [ ${OS_codename} = "buster" ] || [ ${OS_codename} = "bullseye" ]; then

    # Get Current WiFi Country
    current=$(sudo cat /etc/wpa_supplicant/wpa_supplicant.conf | grep country)

    # Rewrite /etc/wpa_supplicant/wpa_supplicant.conf
    sudo sed -i -e s/$current/$COUNTRY/g /etc/wpa_supplicant/wpa_supplicant.conf

# In case of Bookworm or newer
else

    sudo raspi-config nonint do_wifi_country $COUNTRY

fi

## Go back to page
 echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
 echo ""
