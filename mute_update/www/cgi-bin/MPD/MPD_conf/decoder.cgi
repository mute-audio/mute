#!/bin/bash

# decoder.cgi                                    #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 DECODER=$(echo ${QUERY_STRING} | cut -d '=' -f 1 | nkf -Ww --url-input)
 SW=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

if [ ${SW} = "Yes" ]; then

  sudo sed -i -e "/plugin.*\"${DECODER}\"/,/\}/s/\"no\"/\"yes\"/" /etc/mpd.conf

elif [ ${SW} = "No" ]; then

  sudo sed -i -e "/plugin.*\"${DECODER}\"/,/\}/s/\"yes\"/\"no\"/" /etc/mpd.conf

fi

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?decoder"
echo ''
