#!/bin/bash

# samplerate_converter.cgi                       #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 sampleRATE=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input | sed -e 's/\+/\ /g')

sudo sed -i -e "/samplerate_converter\t.*\"/s/\".*\"/\"${sampleRATE}\"/g" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?mpdconfig"
echo ''
