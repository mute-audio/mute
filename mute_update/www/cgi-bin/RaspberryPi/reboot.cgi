#!/bin/bash

# reboot.cgi                                       #
# (C)2023 kitamura_design <kitamura_design@me.com> #

if [ -e "/var/www/cgi-bin/log/reboot_required.log" ]; then
    sudo rm /var/www/cgi-bin/log/reboot_required.log > /dev/null
fi

#Reboot Starting
sudo reboot --no-wall 2>/dev/null 1>/dev/null
