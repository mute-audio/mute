#!/bin/bash

# i2s_dac_install.cgi		                      #
# (C)2023 kitamura_design <kitamura_design@me.com> #

# Check current OS Codename
OS_codename=$(lsb_release -a |  grep Codename | cut -f 2)

if [ ${OS_codename} = "buster" ] || [ ${OS_codename} = "bullseye" ]; then  # In case of Buster, Bullseye etc.
   bootDIR="boot"
else
   bootDIR="boot/firmware"
fi

# Checking config.txt
onboardaudio=$(cat /${bootDIR}/config.txt | egrep --only-matching '#dtparam=audio=on')

# Check config.txt
CURRENT=$(grep '#dtparam=audio=on' -A 1 /${bootDIR}/config.txt | sed -n 2p)

# target DAC
DAC=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

# Install DAC ############### Rewrite config.txt

if [ "$onboardaudio" = "#dtparam=audio=on" ]; then

   if [ -n "$CURRENT" ]; then
   sudo sed -i -e "/^#dtparam=audio=on/,/$CURRENT/ s/$CURRENT/dtoverlay=$DAC/" /${bootDIR}/config.txt
   else
   sudo sed -i -e "/#dtparam=audio=on/adtoverlay=$DAC" /${bootDIR}/config.txt
   fi

else
   sudo sed -i -e "s/dtparam=audio=on/#dtparam=audio=on/" -e "/#dtparam=audio=on/adtoverlay=$DAC" /${bootDIR}/config.txt
fi

echo "Location: /cgi-bin/RaspberryPi/rebooting.cgi"           # Proceed to Reboot
echo

exit 0
