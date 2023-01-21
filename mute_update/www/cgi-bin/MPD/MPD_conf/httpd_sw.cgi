#!/bin/bash

# httpd_sw.cgi                                   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 SW=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

if [ ${SW} = "On" ]; then

  sudo  sed -i -e '/^#HTTPD/,/\}/ s/^#//g' -e '/^HTTPD/,/\}/ s/HTTPD/#HTTPD/' -e '/^#HTTPD/,/\}/ s/^\tbind_to_address/#\tbind_to_address/' -e '/^#HTTPD/,/\}/ s/^\tquality/#\tquality/' -e '/^#HTTPD/,/\}/ s/^\tformat/#\tformat/' -e '/^#HTTPD/,/\}/ s/^\tmax_clients/#\tmax_clients/' /etc/mpd.conf
  wait

elif [ ${SW} = "Off" ]; then

  sudo  sed -i -e '/^#HTTPD/,/\}/ s/^#//g' -e '/^HTTPD/,/\}/ s/^/#/g' /etc/mpd.conf
  wait

fi

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?httpd"
echo ''
