#!/bin/bash

# 64bit_SW.cgi									   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

## 64bit Toggle SW
 kernel=$(uname -m)                              					# 64bit check
                                                		
 if [ "$kernel" = "aarch64" ]; then              					# If kernel is running at 64bit,
     sudo sed -i -e "s/arm_64bit=1/#arm_64bit=1/" /boot/config.txt  # Disable 64bit
 else                                           					# If kernel is running at 32bit,
     sudo sed -i -e "s/#arm_64bit=1/arm_64bit=1/" /boot/config.txt	# Enable 64bit
 fi

## Reboot automatically
echo "location: /cgi-bin/RaspberryPi/rebooting.cgi"
echo
