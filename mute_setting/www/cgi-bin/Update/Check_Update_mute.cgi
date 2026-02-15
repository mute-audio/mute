#!/bin/bash

## Check_Update_mute.cgi
## (C)2026 kitamura_design <kitamura_design@me.com>

### Cancel this process in case of Web Streaming to avoid alsa_output error.
volume=$(mpc -f %file% current | cut -d / -f 1)

if [ "$volume" = "http:" ] || [ "$volume" = "https:" ]; then

    echo "Location: /cgi-bin/Update/Update_caution.cgi"
    echo ''

    exit 1
fi

set -e
set -o pipefail

#### FUNCTION ####

######## [ mute ] Update Check
function genInput_muteUpdate() {
    URL="https://raw.githubusercontent.com/mute-audio/mute/main/packages/package.info"
    pkg_INFO=$(sudo wget --no-check-certificate -q -O - ${URL})
    pkg_VER=$(echo "$pkg_INFO" | grep 'ver=' | sed -e 's/ver=/Ver./g' -e 's/$/<br>/')
    pkg_DTL=$(echo "$pkg_INFO" | sed -n '/info:/,$p' | sed '1d' | sed -e 's/$/<br>/')

    chk_UPDATE=$(echo "$pkg_INFO" | grep "ver=" | sed -e 's/[^0-9]//g')
    chk_CURRENT=$(grep "ver=" /var/www/cgi-bin/etc/mute.conf | sed -e 's/[^0-9]//g')

    if [[ "$chk_UPDATE" -gt "$chk_CURRENT" ]]; then

        echo "[ mute ] Update available.<br>" | sudo tee /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null
        echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null
        echo "$pkg_VER" | sudo tee -a /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null
        echo "$pkg_DTL" | sudo tee -a /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null

    else
        echo "[ mute ] is up to date."
    fi
}

function stream() {
    while read INPUT; do
        echo -n -e "data: ${INPUT}\n\n"
        OUTPUT=${INPUT}
    done

    sleep 1

    echo -n -e "event: close\n"
    echo -n -e "data: ${OUTPUT}\n\n"
}

#### PROCESS ####

### Cancel this process in case of Web Streaming to avoid alsa_output error.
volume=$(mpc -f %file% current | cut -d / -f 1)

if [ "$volume" = "http:" ] || [ "$volume" = "https:" ]; then

    echo "Location: /cgi-bin/Update/Update_caution.cgi"
    echo ''

    exit 1
fi

### Start apt-update streaming
echo "Content-type: text/event-stream; charset=utf-8"
echo "Cache-Control: no-cache"
echo ""

genInput_muteUpdate 2>/dev/null | stream

exit 0
