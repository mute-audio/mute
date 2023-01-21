#!/bin/bash

# audio_buffer_size.cgi                          #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 audioBUFR=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed  -i  -e "/audio_buffer_size/s/\".*\"/\"$audioBUFR\"/g" /etc/mpd.conf
 
echo "Location: /cgi-bin/MPD/MPDupdating.cgi?mpdconfig"
echo ''
