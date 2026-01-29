#!/bin/bash

# git_download_chk.sh
# GitHub Releases Download Checker Script
# (C)2024 kitamura_design <kitamura_design@me.com>

curl --silent --header \
"Accept: application/vnd.github.v3+json" \
https://api.github.com/repos/mute-audio/mute/releases/latest \
| grep -e "\"name\"" -e "\"download_count\"" \
| sed -e 's/^ *//' -e 's/\"//g' -e 's/,//g' -e 's/name: //g'

date

exit 0