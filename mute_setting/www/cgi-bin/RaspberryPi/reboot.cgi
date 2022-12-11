#!/bin/bash

# reboot.cgi                                       #
# (C)2022 kitamura_design <kitamura_design@me.com> #

if [ -e "/var/www/cgi-bin/log/reboot_required.log" ]; then
    sudo rm /var/www/cgi-bin/log/reboot_required.log > /dev/null
fi

#Reboot Starting
sudo reboot
