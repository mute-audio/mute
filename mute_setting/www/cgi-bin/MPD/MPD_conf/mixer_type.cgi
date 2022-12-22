#!/bin/bash

# mixer_type.cgi                                 #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 mixTYPE=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "s/mixer_type\t.*\"/mixer_type\t\t\"${mixTYPE,,}\"/g" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDrestarting.cgi?mpdconfig"
echo ''
