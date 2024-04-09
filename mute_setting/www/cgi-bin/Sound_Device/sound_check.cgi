#!/bin/bash

# sound_check.cgi            					 #
# (C)2022 kitamura_design <kitamura_design@me.com> #


#Checking mpc status
 status=$(mpc status | egrep --only-matching '\[.+\]')

#Clean QUERY_STRING
 HWno=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

query=$(date +%Y%m%d%I%M%S)

if [ "$status" = "[playing]" ]; then

	#suspend playback
	mpc -q stop

	#Play the soundcheck track
	speaker-test -t wav -c2 -l4 -D${HWno} > /dev/null &
	wait

	mpc -q play

else

	#Play the soundcheck track
    speaker-test -t wav -c2 -l4 -D${HWno} > /dev/null &
    wait

fi

echo "Location: /cgi-bin/Sound_Device/Sound_device.cgi"
echo
