#!/bin/bash

# mpc_dbrescan.cgi                                  #
# (C)2026 kitamura_design <kitamura_design@me.com>  #

set -e
set -o pipefail

#### FUNCTION ####

function update_Watcher() {
    while [ $(pgrep mpc) ]; do
        sleep 2
    done
    sudo kill $(pgrep journalctl) >/dev/null
}

function gen_rescanTitles() {
    sudo journalctl -u mpd --no-pager -n 0 -f -o cat --grep 'update:' | \
    sed -u -e "s/updating //g"
}

function stream() {
    count=0
    while read title; do
        count=$((count+1))
        echo -n -e "${title/update/data}\n\n"
    done

    echo -n -e "data: ...Rescan done: ${count}titles\n\n"

    sleep 2

    echo -n -e "event: close\n"
    echo -n -e "data: \n\n"
}

#### PROCESS ####

echo "Content-Type: text/event-stream"
echo "Cache-Control: no-cache"
echo "Connection: keep-alive"
echo ""

mpc rescan -q --wait &
update_Watcher &
gen_rescanTitles 2> /dev/null | stream

exit 0
