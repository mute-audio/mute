#!/bin/bash

# i2s_dac_install.cgi		                      #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Getting current DAC info
#dacinfo=$(cat /proc/asound/card0/pcm0p/sub0/info | grep name | sed -n 1P | sed -e 's/name: //g')
#DEVLIST=$(aplay -l | grep card | cut -d "[" -f 3 | cut -d "]" -f 1 | sed -e 's/^/<option>/g' -e 's/$/<\/option>/g')

# Checking config.txt
onboardaudio=$(cat /boot/config.txt | egrep --only-matching '#dtparam=audio=on')

# Check config.txt
CURRENT=$(grep '#dtparam=audio=on' -A 1 /boot/config.txt | sed -n 2p)

# target DAC
DAC=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

# Install DAC ############### Rewrite /boot/config.txt

if [ "$onboardaudio" = "#dtparam=audio=on" ]; then

   if [ -n "$CURRENT" ]; then
   sudo sed -i -e "/^#dtparam=audio=on/,/$CURRENT/ s/$CURRENT/dtoverlay=$DAC/" /boot/config.txt
   else
   sudo sed -i -e "/#dtparam=audio=on/adtoverlay=$DAC" /boot/config.txt
   fi

else
   sudo sed -i -e "s/dtparam=audio=on/#dtparam=audio=on/" -e "/#dtparam=audio=on/adtoverlay=$DAC" /boot/config.txt
fi

echo "Location: /cgi-bin/RaspberryPi/rebooting.cgi"           # Proceed to Reboot
echo
