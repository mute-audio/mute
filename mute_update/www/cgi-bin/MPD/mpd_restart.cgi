#!/bin/bash

# mpd_restart.cgi                                  #
# (C)2023 kitamura_design <kitamura_design@me.com> #

# Checking mpc status
status=$(mpc status | egrep --only-matching '\[.+\]')

if [ $status = "[playing]" ]; then

        volume=$(mpc -f %file% current | cut -d / -f 1)

        if [ "$volume" = "http:" ] || [ "$volume" = "https:" ]; then

                # get queue No.
                Que_NO=$(mpc -q -f %position% current)

                # suspend playback
                mpc -q stop

                # mpd restart
                sudo systemctl restart mpd

                # resume playback
                mpc -q play ${Que_NO}

        else 

                # suspend playback
                mpc -q toggle

                # mpd restart
                sudo systemctl restart mpd

                # resume playback
                mpc -q toggle

        fi

else
        # mpd reatart
        sudo systemctl restart mpd
fi

echo "Location: /cgi-bin/MPD/MPD.cgi#${QUERY_STRING}"
echo ''

exit 0