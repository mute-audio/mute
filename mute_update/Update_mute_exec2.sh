#!/bin/bash

# Update_mute_exec2.sh            #
# mute (C)2022 kitamura_design    #

#### Copy Update source ####
  ### Move to HOME dir ###
  cd /var/tmp/mute_update 2>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  ### Rewrite log files ###
  sudo cp -RT /var/www/cgi-bin/log ./www/cgi-bin/log 2>/dev/null
  #sudo cp -R /var/www/cgi-bin/log/ ./www/cgi-bin/log 2>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  ### Rewrite mute.conf file ###
  sudo cp /var/www/cgi-bin/etc/mute.conf ./www/cgi-bin/etc/mute.conf 2>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  ### Copy New source files ###
  #sudo chmod -R 777 /var/www
  sudo cp -RT ./www /var/www 2>/dev/null 1>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  #sudo chmod -R 755 /var/www

#### Finalize ####
newVER=$(cat ./update.info | grep ver | cut -d "=" -f 2)
sudo sed -i -e "s/ver.*/ver.${newVER}/" /etc/motd 2>/dev/null 1>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

sudo sed -i -e "s/ver=.*/ver=${newVER}/" /var/www/cgi-bin/etc/mute.conf 2>/dev/null 1>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

Dark_Mode=$(grep darkmode /var/www/cgi-bin/etc/mute.conf)
if [ "$Dark_Mode" = "darkmode=off" ]; then
  sudo cp /var/www/html/css/css_select/main_light.css /var/www/html/css/main.css

elif [ "$Dark_Mode" = "darkmode=on" ]; then
  sudo cp /var/www/html/css/css_select/main_dark.css /var/www/html/css/main.css

elif [ "$Dark_Mode" = "darkmode=auto" ]; then
  sudo cp /var/www/html/css/css_select/main_auto.css /var/www/html/css/main.css

fi

sudo rm -Rf ../mute_update 2>/dev/null 1>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

#### Update Log ####
date +"%Y-%m-%d %H:%M:%S" | sudo tee -a /var/www/cgi-bin/log/update_mute.log > /dev/null

echo "Location: /cgi-bin/loading.cgi?/cgi-bin/RaspberryPi/Raspberrypi.cgi"
echo ''
