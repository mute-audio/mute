#!/bin/bash

# darkmode_sw.cgi		                   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

#Checking Dark Mode Status
darkmodeSTS=$(grep darkmode /var/www/cgi-bin/etc/mute.conf)
MODE=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

if [ "$darkmodeSTS" = "$MODE" ]; then

echo "Location: /cgi-bin/index.cgi"
echo ''

else

    if [ "$MODE" = "darkmode=on" ]; then
        sudo sed -i -e 's/darkmode=.*/darkmode=on/' /var/www/cgi-bin/etc/mute.conf
        sudo cp /var/www/html/css/css_select/main_dark.css /var/www/html/css/main.css

    elif [ "$MODE" = "darkmode=off" ]; then
        sudo sed -i -e 's/darkmode=.*/darkmode=off/' /var/www/cgi-bin/etc/mute.conf
        sudo cp /var/www/html/css/css_select/main_light.css /var/www/html/css/main.css

    elif [ "$MODE" = "darkmode=auto" ]; then
        sudo sed -i -e 's/darkmode=.*/darkmode=auto/' /var/www/cgi-bin/etc/mute.conf
        sudo cp /var/www/html/css/css_select/main_auto.css /var/www/html/css/main.css

    fi

    sleep 1

    echo "Location: /cgi-bin/index.cgi"
    echo ''
fi
