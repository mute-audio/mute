#!/bin/bash

# curl.cgi                                       #
# ©2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 CURL=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

if [ ${CURL} = "Yes" ]; then

  sudo sed -i -e "/CURL/,/\}/s/\"no\"/\"yes\"/" /etc/mpd.conf

elif [ ${CURL} = "No" ]; then

  sudo sed -i -e "/CURL/,/\}/s/\"yes\"/\"no\"/" /etc/mpd.conf

fi

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?inputplugin"
echo
