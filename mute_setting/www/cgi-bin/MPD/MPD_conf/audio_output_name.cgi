#!/bin/bash

# audio_output.cgi                               #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 OUTPUT=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | sed -e "s/\+/\ /g" -e "s/^\ //g" -e "s/\ (.*)//g" | nkf -Ww --url-input)
 DEVICE=$(echo ${QUERY_STRING} | cut -d '(' -f 2 | cut -d ')' -f 1 | nkf -Ww --url-input)

sudo sed -i -e "/^#ALSA$/,/\}/ s/\tname.*\".*\"/\tname\t\t\"${OUTPUT}\"/" /etc/mpd.conf
sudo sed -i -e "/^#ALSA$/,/\}/ s/\tdevice.*\".*\"/\tdevice\t\t\"${DEVICE}\"/" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPD_updating.cgi?output"
echo ''
