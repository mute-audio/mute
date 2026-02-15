#!/bin/bash

# Update_mute_exec.cgi
# (C)2026 kitamura_design <kitamura_design@me.com> #

#### FUNCTION ####

function getInput_muteUpdate() {

    #### Get Update file's URL ####
    muteUPD_URL=$(\
    sudo wget --no-check-certificate -q -O - \
    "https://raw.githubusercontent.com/mute-audio/mute/main/packages/package.info" | \
    grep "url=" | \
    cut -d "=" -f 2 \
    )

    #### Download Update file ####
    cd /var/tmp
    sudo wget --no-check-certificate -qq "${muteUPD_URL}" 2>/dev/null 1>/dev/null

      if [ $? != 0 ]; then
        echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
        echo ''
        exit 1
      fi

    #### Extract file name from URL ####
    UpdateFile=$(echo "$muteUPD_URL" | rev | cut -d "/" -f 1 | rev)

    #### Unzip Update file ####
    sudo unzip -qq $UpdateFile 2>/dev/null 1>/dev/null

       if [ $? != 0 ]; then
        echo "Location: /cgi-bin/Update/Update_error.cgi"
        echo ''
        exit 1
      fi

    sudo rm $UpdateFile 2>/dev/null 1>/dev/null

      if [ $? != 0 ]; then
        echo "Location: /cgi-bin/Update/Update_error.cgi"
        echo ''
        exit 1
      fi

    #### Call Update sub-process
    sudo bash /var/tmp/mute_update/Update_mute_exec2.sh

      if [ $? != 0 ]; then
        echo "Location: /cgi-bin/Update/Update_error.cgi"
        echo ''
        exit 1
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
