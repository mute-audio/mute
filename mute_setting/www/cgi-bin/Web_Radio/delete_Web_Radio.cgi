#!/bin/bash

# delete_Web_Radio.cgi                             #
# (C)2024 kitamura_design <kitamura_design@me.com> #

# Cut Input Data form Web_Radio.cgi to Parts
listTITLE=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | sed -e 's/+/ /g' | nkf -Ww --url-input)
stationNAME=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | sed -e 's/+/ /g' | nkf -Ww --url-input)

# Playlist File Path
plsFILE="/var/lib/mpd/music/Web_Radio/${listTITLE}.m3u"

# Delete staion info from playlist file
sudo sed -i -e "/^#${stationNAME}$/,/^\$/d" "${plsFILE}" > /dev/null

# Delete the playlist file if empty
contentCHK=$(sudo cat "${plsFILE}")

if [ -z ${contentCHK} ]; then
    sudo rm "${plsFILE}"
fi

# Go back to the Page
echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Web_Radio/Web_radio.cgi"
echo ""

exit 0

