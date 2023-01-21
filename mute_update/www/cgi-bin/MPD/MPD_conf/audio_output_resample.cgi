#!/bin/bash

# audio_output.cgi
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 RESMPLE=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/^#ALSA$/,/\}/ s/\tauto_resample.*\".*\"/\tauto_resample\t\"${RESMPLE,,}\"/" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?output"
echo ''
