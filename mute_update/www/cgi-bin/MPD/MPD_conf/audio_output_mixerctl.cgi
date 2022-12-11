#!/bin/bash

# audio_output_mixerctl.cgi                      #
# ©2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 CTL=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/^#ALSA$/,/\}/ s/\tmixer_control.*\".*\"/\tmixer_control\t\"${CTL}\"/" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?output"
echo
