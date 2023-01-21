#!/bin/bash

# 64bit_SW.cgi									   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

## 64bit Toggle SW
 configCHECK=$(sudo grep "arm_64bit" /boot/config.txt)                      # "arm64bit" in Config.txt
 kernel=$(uname -m)                              					        # kernel bit

if [ "$kernel" = "aarch64" ]; then              					        # If kernel is running at 64bit,
    if [ -z $configCHECK ]; then                                            # And if no "arm64bit" line, 
     sudo echo "arm_64bit=1" | sudo tee -a /boot/config.txt > /dev/null     # add "arm_64bit=1"
    fi

    sudo sed -i -e "s/arm_64bit=1/#arm_64bit=1/" /boot/config.txt           # Disable 64bit

else                                           					            # If kernel is running at 32bit,
    if [ -z $configCHECK ]; then                                            # And if no "arm64bit" line, 
     sudo echo "#arm_64bit=1" | sudo tee -a /boot/config.txt > /dev/null    # add "#arm_64bit=1"
    fi

     sudo sed -i -e "s/#arm_64bit=1/arm_64bit=1/" /boot/config.txt          # Enable 64bit

fi

## Reboot automatically
echo "location: /cgi-bin/RaspberryPi/rebooting.cgi"
echo ''
