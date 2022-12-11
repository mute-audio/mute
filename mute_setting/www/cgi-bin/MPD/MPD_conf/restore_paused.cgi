#!/bin/bash

# restore_paused.cgi                             #
# ©2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 rstPAUSE=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/restore_paused.*/s/\".*\"/\"${rstPAUSE,,}\"/g" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?mpdconfig"
echo
