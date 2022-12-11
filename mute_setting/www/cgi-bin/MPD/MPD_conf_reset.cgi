#!/bin/bash

# MPD_conf_reset.cgi         		 			   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

#Checking mpc status
 status=$(mpc status | egrep --only-matching '\[.+\]')

if [ $status = "[playing]" ]; then
	#suspend playback
	 mpc -q stop

	#Revert to default mpd.conf
	 sudo cp -f /var/www/cgi-bin/etc/mpd.conf.mute /etc/mpd.conf

	#mpd restart
	 sudo systemctl restart mpd &
	 wait
else
    #Revert to default mpd.conf
     sudo cp -f /var/www/cgi-bin/etc/mpd.conf.mute /etc/mpd.conf

	#mpd reatart
     sudo systemctl restart mpd &
     wait
fi

echo "Location: /cgi-bin/MPD/MPD.cgi#mpdconfig"
echo ''
