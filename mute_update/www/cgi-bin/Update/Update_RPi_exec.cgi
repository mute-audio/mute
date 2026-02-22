#!/bin/bash

# Update_RPi_exec.cgi
# (C)2026 kitamura_design <kitamura_design@me.com> #

set -e
set -o pipefail

#### FUNCTION ####

function genInput_aptUpgrade() {
    ## Do apt full-upgrade
     sudo apt \
     -o Acquire::Retries=3 \
     -o Dpkg::Options::="--force-confold" \
     -o Dpkg::Options::="--force-confdef" \
     --force-yes -y \
     full-upgrade

    ## Rewrite Update_notice.txt
     stsUPD=$(sudo apt update -qq 2>/dev/null | cut -d"." -f 1)
     echo "${stsUPD}." | sudo tee /var/www/cgi-bin/Update/Update_notice.txt > /dev/null

    ## Update log
     date +"%Y-%m-%d %H:%M:%S" | sudo tee -a /var/www/cgi-bin/log/update.log > /dev/null

    ## Update MPD Version
     mpd -V | sudo tee /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt > /dev/null

    ## Set Reboot Required Badge
     if [ ! -e "/var/www/cgi-bin/log/reboot_required.log" ]; then
        sudo touch /var/www/cgi-bin/log/reboot_required.log > /dev/null
     fi

    ## Clean up
     sudo apt clean 2>/dev/null 1>/dev/null

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

genInput_aptUpgrade 2>/dev/null | stream

exit 0
