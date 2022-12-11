#!/bin/bash

# mpd_restart.cgi								   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

#Checking mpc status
 status=$(mpc status | egrep --only-matching '\[.+\]')

if [ $status = "[playing]" ]; then
	#suspend playback
	 mpc -q pause

	#mpd restart
	 sudo systemctl restart mpd &
	 wait
	 mpc -q play
else
	#mpd reatart
     sudo systemctl restart mpd &
     wait
fi

echo "Location: /cgi-bin/MPD/MPD.cgi#${QUERY_STRING}"
echo ''
