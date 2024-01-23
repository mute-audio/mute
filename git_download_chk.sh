#!/bin/bash

curl --silent --header \
"Accept: application/vnd.github.v3+json" \
https://api.github.com/repos/mute-audio/mute/releases \
| grep -e "\"name\"" -e "\"download_count\"" \
| sed -e 's/^ *//' -e 's/\"//g' -e 's/,//g' -e 's/name: //g'

exit 0