#!/bin/bash

# getcover.cgi                                     #
# (C)2022 kitamura_design <kitamura_design@me.com> #

FILE=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

# Check music_directory
 DIR=$(grep music_directory /etc/mpd.conf | cut -d "\"" -f 2 | sed -e "s/$/\/*\//")

# Exec getcover
 sudo find ${DIR} -type d -exec getcover -f ${FILE} {} \;
 wait

# Go back to page
 echo "Location: /cgi-bin/Other_Settings/other_setting_host.cgi"
 echo ""

exit 0
