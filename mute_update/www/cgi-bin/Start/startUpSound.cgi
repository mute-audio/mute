#!/bin/bash

# startUpSound.cgi : System boot sound playback    #
# (C)2023 kitamura_design <kitamura_design@me.com> #

#Initialize SB32 HW Volume
sudo aplay -q -P -d 1 /var/www/cgi-bin/Start/mute_start.wav > /dev/null

#Play the startup track
sudo aplay -q -P /var/www/cgi-bin/Start/mute_start.wav > /dev/null

exit 0