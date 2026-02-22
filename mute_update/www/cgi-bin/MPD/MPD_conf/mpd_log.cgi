#!/bin/bash

# mpd_log.cgi                                    #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 mpdLOG=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

if [ ${mpdLOG} = "Yes" ]; then

 sudo sed -i -e 's/\#log_file/log_file/g' /etc/mpd.conf

elif [ ${mpdLOG} = "No" ]; then

 sudo sed -i -e 's/\log_file/#log_file/g' /etc/mpd.conf

fi

echo "Location: /cgi-bin/MPD/MPD_updating.cgi?mpdconfig"
echo ''
