#!/bin/bash

# restart_mpdsocket.cgi	                           #
# (C)2022 kitamura_design <kitamura_design@me.com> #

#Checking mpc status
status=$(mpc status | egrep --only-matching '\[.+\]')

if [ $status = "[playing]" ]; then
	#suspend playback
	mpc -q pause

	#disable mpd.socket, and restart playback
	sudo systemctl stop mpd.service
        sudo systemctl start mpd.socket
        sudo systemctl enable mpd.socket
        sudo systemctl start mpd.service
	wait

        mpc -q play
else
	#disable mpd.socket
        sudo systemctl stop mpd.service
        sudo systemctl start mpd.socket
        sudo systemctl enable mpd.socket
        sudo systemctl start mpd.service
        wait
fi

echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
echo ""
