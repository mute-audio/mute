#!/bin/bash

# Update_mute_exec2.sh            #
# mute (C)2023 kitamura_design    #

echo " Updating [ mute ] ..."

#### Copy Update source ####
  ### Move to HOME dir ###
  cd /var/tmp/mute_update 2>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  ### Rewrite log files ###
  echo "Rewrite log files..."
  sudo cp -RT /var/www/cgi-bin/log ./www/cgi-bin/log 2>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  ### Rewrite mute.conf file ###
  echo "Rewrite mute.conf files..."
  sudo cp /var/www/cgi-bin/etc/mute.conf ./www/cgi-bin/etc/mute.conf 2>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  ### Copy New source files ###
  #sudo chmod -R 777 /var/www
  echo "Copy New source files..."
  sudo cp -RT ./www /var/www 2>/dev/null 1>/dev/null

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

 	## Install Update-Check Service & Timer (1.06)
  if [ ! -e /etc/systemd/system/updchk.service ]; then
	    sudo mv /var/www/cgi-bin/Update/updchk.service /etc/systemd/system/updchk.service 2>/dev/null 1>/dev/null

      if [ $? != 0 ]; then
        echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
        echo ''
        exit 1
      fi

	    sudo mv /var/www/cgi-bin/Update/updchk.timer /etc/systemd/system/updchk.timer 2>/dev/null 1>/dev/null

      if [ $? != 0 ]; then
        echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
        echo ''
        exit 1
      fi

	    sudo chmod 644 /etc/systemd/system/updchk.service /etc/systemd/system/updchk.timer

      sudo systemctl daemon-reload
	    sudo systemctl --now enable updchk.service 2>/dev/null 1>/dev/null
	    sudo systemctl --now enable updchk.timer 2>/dev/null 1>/dev/null
  fi

  ## Install Start-Up Sound Service (1.07b)
  if [ ! -e /etc/systemd/system/startUpSound.service ]; then
    echo ""
    echo "Install Start-Up Sound Service..."
	  sudo mv /var/www/cgi-bin/Start/startUpSound.service /etc/systemd/system/startUpSound.service 2>/dev/null 1>/dev/null
  
     if [ $? != 0 ]; then
      echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
      echo ''
      exit 1
    fi

    sudo chmod 644 /etc/systemd/system/startUpSound.service

	  sudo systemctl daemon-reload
	  sudo systemctl enable startUpSound.service 2>/dev/null 1>/dev/null
  fi

	## Activate streaming (1.12.0)
  CHK_streaming=$(sudo grep "server.stream-response-body = 1" /etc/lighttpd/lighttpd.conf || true)

  if [ -z "$CHK_streaming" ]; then 
      echo " Activating Stream-response... "
	    sudo sed -i -e '/server.port.*= */a server.stream-response-body = 1' /etc/lighttpd/lighttpd.conf
  fi

  ## Replace getcover (1.12.0)
  echo ""
  echo " Replacing getcover... "
	sudo gcc -o getcover getcover.c
  sudo mv ./getcover /usr/local/bin/getcover

  if [ $? != 0 ]; then
    echo "Location: /cgi-bin/Update/Update_mute_error.cgi"
    echo ''
    exit 1
  fi

  ## Install DLNA & AirPlay Renderers (1.20)
  echo ''
  echo ' Installing Media Renderers...'

  ## DLNA Renderer (UpMPDcli) 
  echo ""
  echo " DLNA Renderer..."

	# Get OS Code-name
	OS_CODENAME=$(lsb_release -sc)
	echo "Detected OS: ${OS_CODENAME}"

	# Install UpMPDcli and Setting
	if [ "${OS_CODENAME}" = "bullseye" ] || [ "${OS_CODENAME}" = "bookworm" ] || [ "${OS_CODENAME}" = "trixie" ]; then #Version Check
		# Import repository key & Keylist
	    sudo curl -L \
	    https://www.lesbonscomptes.com/pages/lesbonscomptes.gpg \
	    -o /usr/share/keyrings/lesbonscomptes.gpg

	    sudo curl -L \
 	   "https://www.lesbonscomptes.com/upmpdcli/pages/upmpdcli-r${OS_CODENAME}.sources" \
 	   -o /etc/apt/sources.list.d/upmpdcli.sources

		# Install upmpdcli
	    sudo apt update
	    sudo apt -o Acquire::Retries=3 install -y -q upmpdcli

    	# Replace unit file
    	if [ -f /usr/lib/systemd/system/upmpdcli.service ]; then
    	    sudo rm /usr/lib/systemd/system/upmpdcli.service
    	fi
    	sudo cp ./upmpdcli.service /etc/systemd/system/upmpdcli.service
		  sudo cp ./upmpdcli.conf /etc/upmpdcli.conf
		  sudo cp ./mute_icon.png /usr/share/upmpdcli/mute_icon.png

		  #Enable and Start
      sudo systemctl daemon-reload
      sudo systemctl enable --now upmpdcli
	else
    	echo " Skipping UpMPDcli: Unsupported OS version."
	fi

  ## Shairport-sync
  echo ""
  echo "AirPlay Reciever..."

	# Install shairport-sync
	sudo apt -o Acquire::Retries=3 install -y -q shairport-sync

	# AirPlay (Shairport-sync) settings
	sudo systemctl stop shairport-sync

	# Remove old init script if exists
	if [ -f /etc/init.d/shairport-sync ]; then
	    sudo rm /etc/init.d/shairport-sync
	fi

	# Copy config and systemd service files from the same directory
	sudo cp ./shairport-sync.conf /etc/shairport-sync.conf
	sudo cp ./shairport-sync.service /etc/systemd/system/shairport-sync.service	

	# Enable and Start
	echo " Enabling and Starting AirPlay Reciever..."
	sudo systemctl daemon-reload
	sudo systemctl enable --now shairport-sync

  echo ""
  echo " Installing Media Renderers... Done"

#### Finalize ####
#newVER=$(cat ./update.info | grep ver | cut -d "=" -f 2)
newVER=$(grep '^ver=' ./update.info | cut -d '=' -f 2)

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

Dark_Mode=$(grep darkmode /var/www/cgi-bin/etc/mute.conf || true)

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

## Rewrite Update_mute_notice.txt
echo -n "[ mute ] is up to date" | sudo tee /var/www/cgi-bin/Update/Update_mute_notice.txt > /dev/null

#### Update Log ####
date +"%Y-%m-%d %H:%M:%S" | sudo tee -a /var/www/cgi-bin/log/update_mute.log > /dev/null

#echo "Location: /cgi-bin/loading.cgi?/cgi-bin/RaspberryPi/Raspberrypi.cgi"
#echo ''

echo "Location: /cgi-bin/RaspberryPi/rebooting.cgi"
echo ''
