#!/bin/bash

# auto_update.cgi                                #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 autoUPDT=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/auto_update\t.*\"/s/\".*\"/\"${autoUPDT,,}\"/g" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?mpdconfig"
echo ''
