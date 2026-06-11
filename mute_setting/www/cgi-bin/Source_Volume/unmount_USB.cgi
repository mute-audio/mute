#!/bin/bash

# unmount_USB.cgi                                  #
# (C)2026 kitamura_design <kitamura_design@me.com> #

USB_pass=$(echo "${QUERY_STRING}" | nkf -Ww --url-input)
query=$(date +%Y%m%d%I%M%S)
USB_count=$(df -h | grep "/media/" | cut -d "/" -f 5 | wc -l)                     # USB mount number check
busyCHECK=$(sudo lsof "/media/${USB_pass}")

if [ "${USB_count}" -eq 0 ]; then

        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi?$query"        # Escape umount and back to the Page
        echo

elif [ -n "${busyCHECK}" ]; then

        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi?$query"        # Escape umount when busy
        echo

else
        sudo umount "/media/${USB_pass}"                                        # Unmount,and then
        sudo rmdir "/media/${USB_pass}" 2>/dev/null                             # Delete Mount-point

        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi?$query"        # Go back to the Page
        echo
fi

exit 0
