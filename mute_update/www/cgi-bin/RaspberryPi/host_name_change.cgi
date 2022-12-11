#!/bin/bash

# host_name_change.cgi			                 #
# ©2022 kitamura_design <kitamura_design@me.com> #

hostNAME=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)
sudo raspi-config nonint do_hostname ${hostNAME}

#echo "$(cat /etc/hosts)"
#echo "$(cat /etc/hostname)"

echo "location: /cgi-bin/RaspberryPi/rebooting.cgi"
echo ""
