#!/bin/bash

# UTF8.cgi                                       #
# ©2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 UTF8=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

if [ ${UTF8} = "Yes" ]; then

 sudo sed -i -e "/filesystem_charset/s/^#//g" /etc/mpd.conf

elif [ ${UTF8} = "No" ]; then

 sudo sed -i -e "/filesystem_charset/s/^/#/g" /etc/mpd.conf

fi

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?mpdconfig"
echo
