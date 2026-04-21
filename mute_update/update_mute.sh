#!/bin/bash

# +         +
#   m u t e    Updater shell
# +         +
#
# ©2026 kitamura_design <kitamura_design@me.com>

# Check current OS Codename
OS_codename=$(lsb_release -a |  grep Codename | cut -f 2)

if [ ${OS_codename} = "buster" ] || [ ${OS_codename} = "bullseye" ]; then  # In case of Buster, Bullseye etc.
   bootDIR="boot"
else
   bootDIR="boot/firmware"
fi

set -e
#VER=$(cat ./update.info | grep ver | cut -d "=" -f 2)
VER=$(grep '^ver=' ./update.info | cut -d '=' -f 2)

echo ''
echo ' +         +'
echo '   m u t e    RPi-Audio/ MPD Dashboard'
echo " +         +  ver.${VER}"
echo ''
echo " Updater shell for ver.${VER}"
echo ' ©2026 kitamura_design <kitamura_design@me.com>'
echo ''

if [ "$1" = "-y" ]; then
  yn=y

else
  read -p " Updating to ver.${VER}, Are you OK? (Y/n): " yn

fi

case "$yn" in
  ( [yY] ) echo "" ; ;;
  ( [nN] ) echo " Update canceled." ; echo "" ; exit ;;
  ( * ) echo "" ;  ;;
esac

DATE=$(date)

echo " -------- mute Update ( ver.${VER} ) Starts  ${DATE} --------" \
 | sudo tee -a /${bootDIR}/mute_log > /dev/null

#### Copy Updated Source       ####################

echo " Updating [ mute ] ..."

  ### Backup the current log & config files ###
  echo ""
  echo " Backup the current log & config files..."
  sudo cp -RT /var/www/cgi-bin/log ./www/cgi-bin/log  # -T option is available on RpiOS bash
  sudo cp /var/www/cgi-bin/etc/mute.conf ./www/cgi-bin/etc/mute.conf

  ### Copy New source files ###
  echo ""
  echo " Copy New source files..."
  sudo chmod -R 777 /var/www
  sudo cp -RT ./www /var/www
  sudo chmod -R 755 /var/www

 	## Install Update-Check Service & Timer (1.06)
  if [ ! -e /etc/systemd/system/updchk.service ]; then
      echo ""
      echo "Install Update-Check Service & Timer..."
	    sudo mv /var/www/cgi-bin/Update/updchk.service /etc/systemd/system/updchk.service
	    sudo mv /var/www/cgi-bin/Update/updchk.timer /etc/systemd/system/updchk.timer
 
      sudo chmod 644 /etc/systemd/system/updchk.service /etc/systemd/system/updchk.timer

      sudo systemctl daemon-reload
	    sudo systemctl --now enable updchk.service
	    sudo systemctl --now enable updchk.timer
  fi

	## Install Start-Up Sound Service (1.07b)
  if [ ! -e /etc/systemd/system/startUpSound.service ]; then
      echo ""
      echo "Install Start-Up Sound Service..."
	    sudo mv /var/www/cgi-bin/Start/startUpSound.service /etc/systemd/system/startUpSound.service

      sudo chmod 644 /etc/systemd/system/startUpSound.service

	    sudo systemctl daemon-reload
	    sudo systemctl enable startUpSound.service > /dev/null
  fi

	## Activate streaming (1.12.0)
  CHK_streaming=$(sudo grep "server.stream-response-body = 1" /etc/lighttpd/lighttpd.conf || true)

  if [ -z "$CHK_streaming" ]; then
      echo ""
      echo " Activating Stream-response... "
	    sudo sed -i -e '/server.port.*= */a server.stream-response-body = 1' /etc/lighttpd/lighttpd.conf
  fi

  ## Replace getcover (1.12.0)
  echo ""
  echo " Replacing getcover... "
	sudo gcc -o getcover getcover.c
  sudo mv ./getcover /usr/local/bin/getcover

  ## Install DLNA & AirPlay Renderers (1.20)
  echo ''
  echo ' Installing Media Renderers...'

  ## DLNA Renderer (UpMPDcli) 
  echo ""
  echo " DLNA Renderer..."

	# Get OS Code-name
	#OS_CODENAME=$(lsb_release -sc)
  OS_CODENAME="${OS_codename}"

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

echo ""
echo " Updating [ mute ]... Done" \
 | sudo tee -a /${bootDIR}/mute_log > /dev/null

#### Finalize ####################
echo ''
echo " Finalizing Install..."

sudo sed -i -e "s/ver.*/ver.${VER}/" /etc/motd
sudo sed -i -e "s/ver=.*/ver=${VER}/" /var/www/cgi-bin/etc/mute.conf

Dark_Mode=$(grep darkmode /var/www/cgi-bin/etc/mute.conf || true)

if [ "$Dark_Mode" = "darkmode=off" ]; then
  sudo cp /var/www/html/css/css_select/main_light.css /var/www/html/css/main.css

elif [ "$Dark_Mode" = "darkmode=on" ]; then
  sudo cp /var/www/html/css/css_select/main_dark.css /var/www/html/css/main.css

elif [ "$Dark_Mode" = "darkmode=auto" ]; then
  sudo cp /var/www/html/css/css_select/main_auto.css /var/www/html/css/main.css

fi

sudo rm -Rf ../mute_update

echo " Finalizing Install... Done" \
 | sudo tee -a /${bootDIR}/mute_log > /dev/null

#### Update Log ####
date +"%Y-%m-%d %H:%M:%S" \
 | sudo tee -a /var/www/cgi-bin/log/update_mute.log > /dev/null

hostname=$(hostname)

echo ''
echo " [ mute ] is updated successfully."
echo " To confirm update, re-load \" ${hostname}.local \"."
echo ''

DATE=$(date)

echo " --------  mute Update Finished. ${DATE} --------" \
 | sudo tee -a /${bootDIR}/mute_log > /dev/null

exit 0
