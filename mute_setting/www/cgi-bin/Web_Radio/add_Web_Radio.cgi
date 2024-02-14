#!/bin/bash

# add_Web_Radio.cgi                                #
# (C)2024 kitamura_design <kitamura_design@me.com> #

# Web radio directory check
plsDIR="/var/lib/mpd/music/Web_Radio"

if [ ! -d "${plsDIR}" ]; then
    sudo mkdir "${plsDIR}"
fi

# Cut Input Data form Web_Radio.cgi to Parts
listTITLE=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | sed -e 's/+/ /g' | nkf -Ww --url-input)
stationNAME=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | sed -e 's/+/ /g' | nkf -Ww --url-input)
stationURL=$(echo ${QUERY_STRING} | cut -d '&' -f 3 | cut -d '=' -f 2 | nkf -Ww --url-input)

# Set playlist file path
plsPATH="/var/lib/mpd/music/Web_Radio/${listTITLE}.m3u"

# Add staion info to playlist file
sudo tee -a "${plsPATH}" > /dev/null <<PLS
#${stationNAME}
${stationURL}

PLS

# Go back to the Page
echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Web_Radio/Web_radio.cgi"
echo ""

exit 0
