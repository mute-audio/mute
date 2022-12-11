#!/bin/bash

onboardaudio=$(cat /home/pi/dac_list/config.txt | egrep --only-matching '#dtparam=audio=on')
DAC=hifiberry-dacplus

if [ "$onboardaudio" = "#dtparam=audio=on" ]; then

 echo "...On-board audio is already OFF."
 sed --in-place=.bkup -e /#dtparam=audio=on/adtoverlay=$DAC /home/pi/dac_list/config.txt

else

 sed --in-place=.bkup -e 's/dtparam=audio=on/#dtparam=audio=on/' -e /#dtparam=audio=on/adtoverlay=$DAC /home/pi/dac_list/config.txt
 wait

 echo "...Set On-board audio OFF to 'config.txt'."

fi

  echo "...Added DAC \"$DAC\" to config.txt, reboot."
