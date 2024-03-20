#!/bin/bash

# start.cgi : Initializing mute                    #
# (C)2024 kitamura_design <kitamura_design@me.com> #

#### ALSA Check, if dead, reactivate
alsaSTS=$(systemctl status alsa-state.service | grep Active: | cut -d ":" -f 2 | cut -d " " -f 3)

if [ ${alsaSTS} = "(dead)" ]; then
    sudo systemctl start alsa-state.service
fi

cat << HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
HTML

#Checking MPD installed
checkMPD=$(systemctl status mpd | grep mpd.service | sed -n 1p | cut -d " " -f2)

#If MPD installed, show RaspberryPi menu
if [ "$checkMPD" = "mpd.service" ]; then

  cat <<HTML
  <head>
    <link rel="stylesheet" type="text/css" href="/css/main.css">
    <meta http-equiv="refresh" content="0.5; URL=/cgi-bin/RaspberryPi/Raspberrypi.cgi">
  </head>
HTML

#If MPD not installed, show MPD install menu
else
  cat <<HTML
  <head>
    <link rel="stylesheet" type="text/css" href="/css/main.css">
    <meta http-equiv="refresh" content="0.5; URL=/cgi-bin/MPD/MPD_not_installed.cgi">
  </head>
HTML

fi

cat <<HTML
  <body>
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Loading ...</div>
        <div class="progress-bar-base">
        <div class="progress-value-loading"></div>
        </div>
     </div>
   </div>
  </body>

</html>
HTML
