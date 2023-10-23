#!/bin/bash

# Update_MPD_exec.cgi                           #
# (C)2023 kitamura_design <kitamura_design@me.com> #

#### Re-install newer Ver. of MPD  ####

  newPKG=$(sudo apt list -qq -a mpd 2>/dev/null | grep -B 1 'mpd/.*now' | sed -n 1p | cut -d " " -f 1)

  sudo apt install --reinstall $newPKG 2>/dev/null 1>/dev/null

    if [ $? != 0 ]; then
      echo "Location: /cgi-bin/Update/Update_error.cgi"
      echo ''
      exit 1
    fi

  sudo systemctl restart mpd

    if [ $? != 0 ]; then
      echo "Location: /cgi-bin/Update/Update_error.cgi"
      echo ''
      exit 1
    fi

  mpd -V | sudo tee /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt > /dev/null

    if [ $? != 0 ]; then
      echo "Location: /cgi-bin/Update/Update_error.cgi"
      echo ''
      exit 1
    fi

exit 0