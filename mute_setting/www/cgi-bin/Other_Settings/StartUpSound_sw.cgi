#!/bin/bash

# StartUpSound_sw.cgi                      #
# (C)2023 kitamura_design <kitamura_design@me.com> #

if [[ -L /etc/systemd/system/multi-user.target.wants/startUpSound.service ]]; then

sudo systemctl disable startUpSound.service > /dev/null

echo "Location: /cgi-bin/Other_Settings/${QUERY_STRING}"
echo ''

else

sudo systemctl enable startUpSound.service > /dev/null

echo "Location: /cgi-bin/Other_Settings/${QUERY_STRING}"
echo ''

fi