#!/bin/bash

# mount_NAS.cgi                                  #
# (C)2026 kitamura_design <kitamura_design@me.com> #

# Cut Input Data form Source_info_NAS/NONAS.cgi to Parts
NAME=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | nkf -Ww --url-input)
ADRS=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | nkf -Ww --url-input)
VERS=$(echo ${QUERY_STRING} | cut -d '&' -f 3 | cut -d '=' -f 2 | nkf -Ww --url-input)
USER=$(echo ${QUERY_STRING} | cut -d '&' -f 4 | cut -d '=' -f 2 | nkf -Ww --url-input)
PASS=$(echo ${QUERY_STRING} | cut -d '&' -f 5 | cut -d '=' -f 2 | nkf -Ww --url-input)

#### Input validation - reject anything outside expected format
NG_CHARS='[[:space:];|&$`"'\''\<>(){}*?~!#]'
NG_CHARS_NAME="${NG_CHARS%]}/.]"

if [[ "${NAME}" =~ ${NG_CHARS_NAME} ]]; then
    echo "Location: /cgi-bin/Source_Volume/NAS_mount_error.cgi"
    echo ""
    exit 1
fi

if [[ "${ADRS}" =~ ${NG_CHARS} ]]; then
    echo "Location: /cgi-bin/Source_Volume/NAS_mount_error.cgi"
    echo ""
    exit 1
fi

if [[ ! "${VERS}" =~ ^vers=[0-9.]+$ ]]; then
    echo "Location: /cgi-bin/Source_Volume/NAS_mount_error.cgi"
    echo ""
    exit 1
fi

MOUNT_OPTS="${VERS},username=${USER:-guest},password=${PASS},rw,iocharset=utf8"
FSTAB="//${ADRS} /mnt/${NAME} cifs _netdev,${MOUNT_OPTS} 0 0"
MOUNT_POINT="/mnt/${NAME}"

#### Clean-up any existing fstab entry for this mount point, regardless of IP
fstab_CHK=$(grep -F " ${MOUNT_POINT} " /etc/fstab)

 if [ -n "$fstab_CHK" ]; then
    sudo sed -i -e "\@[[:space:]]${MOUNT_POINT}[[:space:]]@d" /etc/fstab
 fi

#### If NAS already mounted to the same Mount-Point, unmount once
MNT_check=$(df -ah | egrep --only-matching "/mnt/${NAME}")

 if [ -n "$MNT_check" ]; then
    sudo umount "/mnt/${NAME}"                                    # Unmount
 fi

#### Mount-Point check
 if [ ! -e "/mnt/${NAME}" ]; then
    sudo mkdir "/mnt/${NAME}"
 fi

#### Mount NAS
 sudo mount -t cifs -o "${MOUNT_OPTS}" "//${ADRS}" "/mnt/${NAME}"

#### Mount check
 if [ $? = 0 ]; then
#    sudo sed -i -e "/# a swapfile/i${FSTAB//\//\\/}" /etc/fstab     # Write mount setting to fstab
     echo ${FSTAB} | sudo tee -a /etc/fstab >/dev/null               # Write mount setting to fstab
 else                                                               # If failed to mount NAS, Exit with deleting the mount-point dir.
    sudo rmdir "/mnt/${NAME}"                                         # Delete a mount point dir.
    echo "Location: /cgi-bin/Source_Volume/NAS_mount_error.cgi"     # Go to the error Page
    echo ""
    exit 1
 fi

#### MPD Dir. check
MPD_check=$(dpkg -l mpd | grep --only-matching mpd)

 if [ "$MPD_check" = "mpd" ]; then
    sudo chown mpd:audio  "/mnt/${NAME}"
    MPD_link="/var/lib/mpd/music/${NAME}"
     if [ -e "$MPD_link" ]; then
        sudo unlink "$MPD_link"
        sudo ln -s "/mnt/${NAME}" "$MPD_link"              # Re-Make link to mpd music dir.
     else
        sudo ln -s "/mnt/${NAME}" "$MPD_link"              # Make link to mpd music dir.
     fi
 fi

 # Go back to the Page
echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Source_Volume/Source_volume.cgi"
echo ""

