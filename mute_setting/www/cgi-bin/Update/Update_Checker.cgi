#!/bin/bash

## Update_Checker.cgi
## (C)2025 kitamura_design <kitamura_design@me.com>

### Cancel this process in case of Web Streaming to avoid alsa_output error.
volume=$(mpc -f %file% current | cut -d / -f 1)

if [ "$volume" = "http:" ] || [ "$volume" = "https:" ]; then

    echo "Location: /cgi-bin/Update/Update_caution.cgi"
    echo ''

    exit 1
fi

######## [ mute ] Update Check
URL="https://raw.githubusercontent.com/mute-audio/mute/main/packages/package.info"
pkg_INFO=$(sudo wget --no-check-certificate -q -O - ${URL})
pkg_VER=$(echo "$pkg_INFO" | grep 'ver=' | sed -e 's/ver=/Ver./g' -e 's/$/<br>/')
pkg_DTL=$(echo "$pkg_INFO" | sed -n '/info:/,$p' | sed '1d' | sed -e 's/$/<br>/')

chk_UPDATE=$(echo "$pkg_INFO" | grep "ver=" | sed -e 's/[^0-9]//g')
chk_CURRENT=$(grep "ver=" /var/www/cgi-bin/etc/mute.conf | sed -e 's/[^0-9]//g')

if [[ "$chk_UPDATE" -gt "$chk_CURRENT" ]]; then

    echo "[ mute ] Update available.<br>" | sudo tee /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null
    echo "<br>" | sudo tee /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null
    echo "$pkg_VER" | sudo tee -a /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null
    echo "$pkg_DTL" | sudo tee -a /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null

fi

####### MPD Update Check
currentMPD_List=$(cat /var/www/cgi-bin/Update/Update_MPD_notice.txt)
mpd_List=$(sudo apt list -a -qq mpd 2>/dev/null | grep -B 1 'mpd.*now')

if [ "$currentMPD_List" != "$mpd_List" ]; then

    echo $mpd_List | sudo tee /var/www/cgi-bin/Update/Update_MPD_notice.txt > /dev/null

fi

######## RaspberryPi OS Update Check
stsUPD=$(sudo apt update -qq 2>/dev/null | cut -d "." -f 1)
apt_list=$(sudo apt list --upgradable -qq 2>/dev/null | sed -e "s/$/<br>/g")

if [ -n "$stsUPD" ]; then

    if [ "$stsUPD" != "All packages are up to date" ]; then

        echo "${stsUPD}." | sudo tee /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "$apt_list" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt # > /dev/null
    fi

fi

echo "Location: /cgi-bin/Update/Update.cgi"
echo ''

exit 0