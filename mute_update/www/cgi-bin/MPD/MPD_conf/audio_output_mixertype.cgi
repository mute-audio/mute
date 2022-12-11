#!/bin/bash

# audio_output_mixertype.cgi                     #
# ©2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 MIXER=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/^#ALSA$/,/\}/ s/\tmixer_type.*\".*\"/\tmixer_type\t\"${MIXER,,}\"/" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?output"
echo
