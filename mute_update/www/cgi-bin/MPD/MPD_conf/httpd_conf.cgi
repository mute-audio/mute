#!/bin/bash

# httpd_conf.cgi	                             #
# ©2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 NAME=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | sed -e "s/\+/\ /g" -e "s/^\ //g" -e "s/\ (.*)//g" | nkf -Ww --url-input)
 PORT=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | nkf -Ww --url-input)
 ENCODER=$(echo ${QUERY_STRING} | cut -d '&' -f 3 | cut -d '=' -f 2 | nkf -Ww --url-input)
 BPS=$(echo ${QUERY_STRING} | cut -d '&' -f 4 | cut -d '=' -f 2 | nkf -Ww --url-input)

sudo sed -i -e "/^#HTTPD$/,/\}/ s/\tname.*\".*\"/\tname\t\t\"${NAME}\"/" /etc/mpd.conf
sudo sed -i -e "/^#HTTPD$/,/\}/ s/\tencoder.*\".*\"/\tencoder\t\t\"${ENCODER}\"/" /etc/mpd.conf
sudo sed -i -e "/^#HTTPD$/,/\}/ s/\tport.*\".*\"/\tport\t\t\"${PORT}\"/" /etc/mpd.conf
sudo sed -i -e "/^#HTTPD$/,/\}/ s/\tbitrate.*\".*\"/\tbitrate\t\t\"${BPS}\"/" /etc/mpd.conf

echo "Location: /cgi-bin/MPD/MPDupdating.cgi?httpd"
echo
