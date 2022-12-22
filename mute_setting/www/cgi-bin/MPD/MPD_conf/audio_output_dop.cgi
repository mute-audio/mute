#!/bin/bash

# audio_output.cgi                               #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 DOP=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/^#ALSA$/,/\}/ s/\tdop.*\".*\"/\tdop\t\t\"${DOP,,}\"/" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?output"
echo ''
