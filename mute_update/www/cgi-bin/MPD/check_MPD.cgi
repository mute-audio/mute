#!/bin/bash

# check_MPD.cgi         			 #
# (C)2022 kitamura_design <kitamura_design@me.com> #

### Get infomations
 checkMPD=$(systemctl status mpd | grep mpd.service | sed -n 1p | cut -d " " -f2)
 checkMPDSCRIBBLE=$(systemctl status mpdscribble | grep mpdscribble.service | sed -n 1p | cut -d " " -f2)
 checkMPC=$(dpkg -l | grep -w mpc | cut -d " " -f3)

query=$(date +%Y%m%d%I%M%S)

### MPD check
if [ "$checkMPD" = "mpd.service" ] && [ "$checkMPDSCRIBBLE" = "mpdscribble.service" ] && [ "$checkMPC" = "mpc" ]; then

	echo "Location: /cgi-bin/MPD/MPD.cgi"
	echo

else

        echo "Location: /cgi-bin/MPD/MPD_not_installed.cgi"
        echo

fi
