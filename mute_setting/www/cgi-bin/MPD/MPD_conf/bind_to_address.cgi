#!/bin/bash

# bind_to_address.cgi                            #
# ©2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 bindADD=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/HTTPD/,/}/ !s/bind_to_address.*\"/bind_to_address\t\t\"${bindADD}\"/g" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?mpdconfig"
echo
