#!/bin/bash

# Update_exec.cgi		                             #
# ©2022 kitamura_design <kitamura_design@me.com> #

## Do Update by apt
 sudo apt -o Acquire::Retries=3 -y -qq full-upgrade 2>/dev/null 1>/dev/null

  ## Error Check
  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_error.cgi"
    echo ''
    exit 1
  fi

## Update log
 date +"%Y-%m-%d %H:%M:%S" | sudo tee -a /var/www/cgi-bin/log/update.log > /dev/null

## Update MPD Version
 mpd -V | sudo tee /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt > /dev/null

## Set Reboot Required Badge
 if [ ! -e "/var/www/cgi-bin/log/reboot_required.log" ]; then
    sudo touch /var/www/cgi-bin/log/reboot_required.log > /dev/null
 fi

## Clean up
 sudo apt clean 2>/dev/null 1>/dev/null

## Go back to the Page
 echo "Location: /cgi-bin/loading.cgi?/cgi-bin/RaspberryPi/Raspberrypi.cgi"           
 echo ''
