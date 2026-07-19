#!/bin/bash

# Unmount_NAS.cgi                                  #
# (C)2026 kitamura_design <kitamura_design@me.com> #

MountDir=$(echo ${QUERY_STRING} | cut -d "/" -f 3)

sudo umount "/mnt/${MountDir}"                                    # Unmount

#### umount error check

if [ $? = 0 ]; then                                     # If succeed to un-mounted,
         sudo sed -i -e "/\/mnt\/${MountDir}/d" /etc/fstab   # Delete mount setting form fatab

        # Check MPD installed
        checkMPD=$(dpkg -l mpd | grep --only-matching mpd)

        if [ "$checkMPD" = "mpd" ]; then
        sudo unlink "/var/lib/mpd/music/${MountDir}"              # Delete a link to mpd's music dir.
        fi

        sudo rmdir "/mnt/${MountDir}"                             # Delete a mount point dir.
        wait

        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi"       # Go back to the Page
        echo ""
else                                                    # If failed to un-mount NAS, do NOTHING
        echo "Location: /cgi-bin/Source_Volume/Source_volume.cgi"       # Go back to the Page
        echo ""
fi

