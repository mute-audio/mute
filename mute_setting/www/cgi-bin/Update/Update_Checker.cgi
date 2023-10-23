#!/bin/bash

### Cancel this process in case of Web Streaming to avoid alsa_output error.

volume=$(mpc -f %file% current | cut -d / -f 1)

if [ "$volume" = "http:" ] || [ "$volume" = "https:" ]; then

    echo "Location: /cgi-bin/Update/Update.cgi"
    echo ''

    exit 1
fi

######## [ mute ] Update Check

ver_UPDATE=$(\
sudo wget --no-check-certificate -q -O - "https://www.dropbox.com/s/9op8f7ras6s4a94/update.info" \
    | grep "ver=" | sed -e 's/[^0-9]//g'\
)

ver_CURRENT=$(\
grep "ver=" /var/www/cgi-bin/etc/mute.conf \
    | sed -e 's/[^0-9]//g'\
)

if [[ "$ver_UPDATE" -gt "$ver_CURRENT" ]]; then

    echo "[ mute ] Update available" | sudo tee /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null

fi

####### MPD Update Check

currentMPD_List=$(cat /var/www/cgi-bin/Update/Update_MPD_notice.txt)
mpd_List=$(sudo apt list -a -qq mpd 2>/dev/null | grep -B 1 'mpd.*now')

if [ "$currentMPD_List" != "$mpd_List" ]; then

    echo $mpd_List | sudo tee /var/www/cgi-bin/Update/Update_MPD_notice.txt > /dev/null
fi

######## RaspberryPi OS Update Check

stsUPD=$(sudo apt update -qq 2>/dev/null | cut -d"." -f 1)
apt_list=$(sudo apt list --upgradable -qq 2>/dev/null | sed -e "s/$/<br>/g")

if [ "$stsUPD" != "All packages are up to date" ]; then

        echo "${stsUPD}." | sudo tee /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "$apt_list" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt # > /dev/null

fi

echo "Location: /cgi-bin/Update/Update.cgi"
echo ''

exit 0