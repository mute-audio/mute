#!/bin/bash

# mount_NAS.cgi                                  #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Cut Input Data form Source_info_NAS/NONAS.cgi to Parts
NAME=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | nkf -Ww --url-input)
ADRS=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | nkf -Ww --url-input)
VERS=$(echo ${QUERY_STRING} | cut -d '&' -f 3 | cut -d '=' -f 2 | nkf -Ww --url-input)
USER=$(echo ${QUERY_STRING} | cut -d '&' -f 4 | cut -d '=' -f 2 | nkf -Ww --url-input)
PASS=$(echo ${QUERY_STRING} | cut -d '&' -f 5 | cut -d '=' -f 2 | nkf -Ww --url-input)

FSTAB="//${ADRS} /mnt/${NAME} cifs _netdev,${VERS},username=${USER:- guest},password=${PASS},rw,iocharset=utf8 0 0"

#### Clean-up fstab even if setting already exits
fstab_CHK=$(grep --only-matching "$FSTAB" /etc/fstab)

 if [ -n "$fstab_CHK" ]; then
    sudo sed -i -e "/${FSTAB//\//\\/}/d" /etc/fstab
 fi

#### If NAS already mounted to the same Mount-Point, unmount once
NNT_check=$(df -ah | egrep --only-matching '/mnt/${NAME}')

 if [ -n "$MNT_check" ]; then
    sudo umount /mnt/${NAME}                                    # Unmount
 fi

#### Mount-Point check
 if [ ! -e /mnt/${NAME} ]; then
    sudo mkdir /mnt/${NAME}
 fi

#### Mount NAS
 sudo mount -o ${VERS},username=${USER:- guest},password=${PASS},rw,iocharset=utf8 //${ADRS} /mnt/${NAME}        # Mount NAS

#### Mount check
 if [ $? = 0 ]; then
#    sudo sed -i -e "/# a swapfile/i${FSTAB//\//\\/}" /etc/fstab     # Write mount setting to fstab
     echo ${FSTAB} | sudo tee -a /etc/fstab >/dev/null               # Write mount setting to fstab
 else                                                               # If failed to mount NAS, Exit with deleting the mount-point dir.
    sudo rmdir /mnt/${NAME}                                         # Delete a mount point dir.
    echo "Location: /cgi-bin/Source_Volume/NAS_mount_error.cgi"     # Go to the error Page
    echo ""
 fi

#### MPD Dir. check
MPD_check=$(dpkg -l mpd | grep --only-matching mpd)

 if [ "$MPD_check" = "mpd" ]; then
    sudo chown mpd:audio /mnt/nas
    MPD_link="/var/www/mpd/music/${NAME}"
     if [ -e "$MPD_link" ]; then
        sudo unlink /var/lib/mpd/music/${NAME}
        sudo ln -s /mnt/${NAME} /var/lib/mpd/music/${NAME}              # Re-Make link to mpd music dir.

     else
        sudo ln -s /mnt/${NAME} /var/lib/mpd/music/${NAME}              # Make link to mpd music dir.
     fi
 #else
 fi

 # Go back to the Page
echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Source_Volume/Source_volume.cgi"
echo ""

