#!/bin/bash

# stream_apt_Update.cgi
# (C)2026 kitamura_design <kitamura_design@me.com> #

set -e
set -o pipefail

#### FUNCTION ####

function genInput_aptUpdate() {
    sudo apt update
}

function stream() {
    while read INPUT; do
        echo -n -e "data: ${INPUT}\n\n"
        OUTPUT=${INPUT}
    done

    if [ "${OUTPUT}" != "All packages are up to date." ]; then
       apt_List=$(sudo apt list --upgradable -qq 2>/dev/null | sed -e "s/$/<br>/g")
       echo "${OUTPUT}" | sudo tee /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
       echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
       echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
       echo "$apt_list" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt
    fi

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

genInput_aptUpdate 2> /dev/null | stream

exit 0
