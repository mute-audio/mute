#!/bin/bash

# unmount_USB.cgi                                  #
# (C)2022 kitamura_design <kitamura_design@me.com> #

USB_pass=$(echo ${QUERY_STRING} | nkf -Ww --url-input)
query=$(date +%Y%m%d%I%M%S)
USB_count=$(df -h | grep /media/ | cut -d "/" -f 5 | wc -l)                     # USB mount number check
busyCHECK=$(sudo lsof /media/$USB_pass)

if [ $USB_count = 0 ]; then

        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi?$query"        # Escape umount and back to the Page
        echo

elif [ -n "$busyCHECK" ]; then

        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi?$query"        # Escape umount when busy
        echo

else
        sudo umount /media/"$USB_pass"                                          # Unmount
        wait

        sudo rmdir --ignore-fail-on-non-empty /media/"$USB_pass"                # Delete Mount-point

        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi?$query"        # Go back to the Page
        echo
fi
