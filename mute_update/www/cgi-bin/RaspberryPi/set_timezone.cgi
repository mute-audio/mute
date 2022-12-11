#!/bin/bash

# set_timezone.cgi                                 #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 timezone=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo timedatectl set-timezone ${timezone}

# Go back to the Page
 echo "Location: /cgi-bin/RaspberryPi/Raspberrypi.cgi"
 echo ""
