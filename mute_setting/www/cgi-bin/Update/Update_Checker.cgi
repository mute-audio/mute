#!/bin/bash

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