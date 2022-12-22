#!/bin/bash

# host_name_change.cgi			                 #
# (C)2022 kitamura_design <kitamura_design@me.com> #

hostPWD=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)
(echo \"${hostPWD}\" ; echo \"${hostPWD}\") | sudo passwd -q

#echo "${hostPWD}"

echo "location: /cgi-bin/RaspberryPi/rebooting.cgi"
echo ""
