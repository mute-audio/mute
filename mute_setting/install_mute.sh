#!/bin/bash

# +         +
#   m u t e    Installer shell
# +         +
#
# (C)2022 kitamura_design <kitamura_design@me.com>

set -e
VER=$(cat ./www/cgi-bin/etc/mute.conf | grep ver | cut -d "=" -f 2)

echo ''
echo ' +         +'
echo '   m u t e    RPi-Audio/ MPD Dashboard'
echo " +         +  ver.${VER}"
echo ''
echo " Installer shell for ver.${VER}"
echo ' ©2022 kitamura_design <kitamura_design@me.com>'
echo ''
echo ' PROCEDURES'
echo ''
echo ' 1 - Install lighttpd (Web Server middle-ware)'
echo ' 2 - User group & Permission settings'
echo ' 3 - Enable CGI'
echo ' 4 - Install dependencies - nkf, lsof, bc, pmount, getcover'
echo ' 5 - Copy [ mute ] source'
echo ' 6 - Finalize - Clean up the sources and this script'
echo ''

if [ "$1" = "-y" ]; then
  yn=y

else
  read -p " Are you ready? (Y/n): " yn

fi

case "$yn" in
  ( [yY] ) echo "" ; ;;
  ( [nN] ) echo " Install canceled." ; echo "" ; exit ;;
  ( * ) echo "" ;  ;;
esac

DATE=$(date)

echo " -------- mute install Starts  ${DATE} --------" | sudo tee -a /boot/mute_log > /dev/null

#### lightttpd install 	###############################

echo ' 1 - Install lighttpd (Web Server middle-ware)' | sudo tee -a /boot/mute_log

set +e

CHK_lighttpd=$(dpkg -l | grep lighttpd | head -n 1 | cut -d " " -f3)

set -e

if [ "$CHK_lighttpd" = "lighttpd" ]; then

	echo " lighttpd is already installed. Installer will skip this process.." | sudo tee -a /boot/mute_log
else
	echo " Updating the package index files..."
	sudo apt clean && sudo apt update
	wait
        echo " Updating the package index files... Done" | sudo tee -a /boot/mute_log > /dev/null

        echo ''
	echo " Installing lighttpd..."
	sudo apt -o Acquire::Retries=3 -y -q install lighttpd
	wait
        echo " Installing lighttpd... Done" | sudo tee -a /boot/mute_log > /dev/null

	echo ''
	echo " Starting & Enabling lighttpd..."
	sudo systemctl daemon-reload
	sudo systemctl enable --now lighttpd | sudo tee -a /boot/mute_log
	wait
fi

#### User group & Permission setting	 ##############

echo ''
echo ' 2 - User Group & Permission settings' | sudo tee -a /boot/mute_log

set +e

CHK_groups_audio=$(groups www-data | grep --only-matching audio)

set -e

if [ "$CHK_groups_audio" = "audio" ]; then

	echo " Checking User group  -- OK." | sudo tee -a /boot/mute_log
else
	echo " Changing User group setting..."
	sudo gpasswd -a www-data audio  | sudo tee -a /boot/mute_log
        echo " Changing User group setting... Done"  | sudo tee -a /boot/mute_log > /dev/null
fi

set +e

CHK_groups_sudo=$(sudo cat /etc/sudoers | grep www-data | grep --only-matching "NOPASSWD: ALL")

set -e

if [ "$CHK_groups_sudo" = "NOPASSWD: ALL" ]; then
        echo " Checking Permission -- OK." | sudo tee -a /boot/mute_log
else
	echo " Changing Permission setting..."
	echo "www-data ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers  > /dev/null
fi

#### Enable CGI		 #############################
echo ''
echo ' 3 - Enable CGI'  | sudo tee -a /boot/mute_log

set +e

CHK_cgi_active=$(ls /etc/lighttpd/conf-enabled | grep 10-cgi.conf)

set -e

if [ "$CHK_cgi_active" = "10-cgi.conf" ]; then

	echo " CGI already activated. Installer will skip this process.."  | sudo tee -a /boot/mute_log

else
	echo " Enabling CGI..."

	sudo lighttpd-enable-mod cgi | sudo tee -a /boot/mute_log > /dev/null
	wait

	{
	echo '# /usr/share/doc/lighttpd/cgi.txt'
	echo ''
	echo 'server.modules += ( "mod_cgi" )'
	echo ''
	echo '$HTTP["url"] =~ "^/cgi-bin/" {'
	echo '	alias.url += ( "/cgi-bin/" => "/var/www/cgi-bin/" )'
	echo '	cgi.assign = ( ".cgi" => "/usr/bin/bash" )'
	echo '}'
	echo ''
	echo '## Warning this represents a security risk, as it allow to execute any file'
	echo '## with a .pl/.py even outside of /usr/lib/cgi-bin.'
	echo '#'
	echo '#cgi.assign      = ('
	echo '#       ".pl"  => "/usr/bin/perl",'
	echo '#       ".py"  => "/usr/bin/python",'
	echo '#)'
	} | sudo tee /etc/lighttpd/conf-enabled/10-cgi.conf > /dev/null

	wait

	sudo service lighttpd force-reload
	wait

	echo ''
	echo " Restarting lighttpd to activate CGI..."

	sleep 3
	sudo systemctl restart lighttpd
	wait
        echo " Restarting lighttpd to activate CGI... Done" | sudo tee -a /boot/mute_log > /dev/null
fi

#### Install dependencies 	####################

echo ''
echo ' 4 - Install dependencies - nkf, lsof, bc, pmount, getcover'  | sudo tee -a /boot/mute_log

#### nkf ####
set +e

CHK_nkf=$(dpkg -l | grep nkf | head -n 1 | cut -d " " -f3)

set -e

if [ "$CHK_nkf" = "nkf" ]; then
        echo " nkf is already installed. Installer will skip this process.." | sudo tee -a /boot/mute_log
else
	echo ''
	echo " Installing nkf..."
	sudo apt -o Acquire::Retries=3 install -y -q nkf
	wait
        echo " Installing nkf... Done" | sudo tee -a /boot/mute_log > /dev/null
fi

#### lsof ####
set +e

CHK_lsof=$(dpkg -l | grep lsof | head -n 1 | cut -d " " -f3)

set -e

if [ "$CHK_lsof" = "lsof" ]; then
        echo " lsof is already installed. Installer will skip this process.." | sudo tee -a /boot/mute_log
else
	echo ''
        echo " Installing lsof..."
        sudo apt -o Acquire::Retries=3 install -y -q lsof
        wait
        echo " Installing lsof... Done" | sudo tee -a /boot/mute_log > /dev/null
fi

#### bc ####
set +e

CHK_bc=$(dpkg -l | grep bc | head -n 1 | cut -d " " -f3)

set -e

if [ "$CHK_bc" = "bc" ]; then
         echo " bc is already installed. Installer will skip this process.." | sudo tee -a /boot/mute_log
else
	echo ''
        echo " Installing bc..."
        sudo apt -o Acquire::Retries=3 install -y -q bc
        wait
        echo " Installing bc... Done" | sudo tee -a /boot/mute_log > /dev/null
fi

#### pmount ####
set +e

CHK_pmount=$(dpkg -l | grep pmount | head -n 1 | cut -d " " -f3)

set -e

if [ "$CHK_pmount" = "pmount" ]; then
        echo " pmount is already installed. Installer will skip this process.." | sudo tee -a /boot/mute_log
else
        echo ''
        echo " Installing pmount..."
        sudo apt -o Acquire::Retries=3 install -y -q pmount
        wait

	sudo cp ./99-usb-mount.rules /etc/udev/rules.d/99-usb-mount.rules	#USB-drive auto-mount setting1

	sudo cp ./usb-mount@.service /etc/systemd/system/usb-mount@.service	#Daemonaize udiskie
	sudo systemctl daemon-reload						#
        echo " Installing pmount... Done" | sudo tee -a /boot/mute_log > /dev/null
fi

#### getcover ####

if [ -e /usr/local/bin/getcover ]; then
        echo " getcover is already installed. Installer will skip this process.." | sudo tee -a /boot/mute_log
else
        echo ''
        echo " Installing getcover..."
	sudo wget -q --no-check-cert https://www.openaudiolab.com/app/download/14111530129/getcover20181203.tar.gz
        wait
	sudo gunzip getcover20181203.tar.gz && sudo tar xvf getcover20181203.tar --no-same-owner
	wait
	sudo mv ./getcover/getcover /usr/local/bin
        echo " Installing getcover... Done" | sudo tee -a /boot/mute_log > /dev/null
fi


#### Install [ mute ] Source		####################

echo ''
echo " 5 - Copy [ mute ] source" | sudo tee -a /boot/mute_log

set +e

hostname=$(hostname)

set -e

if [ -e /var/www/cgi-bin/etc/mute.conf ]; then

    echo " [ mute ] source exists, you can use [ mute ] already." | sudo tee -a /boot/mute_log
	echo " To control [ mute ], access \" ${hostname}.local \" via web browser from your PC/Tablet."
    echo ''
    echo ' --------  mute install Finished. --------' | sudo tee -a /boot/mute_log > /dev/null

else

	echo " Copying [ mute ] source..."
	sudo chmod -R 777 /var/www
	#sudo cp -RT ./www /var/www
	sudo cp -R ./www/ /var/www
	wait
    sudo chmod -R 755 /var/www
    echo " Copying [ mute ] source... Done" | sudo tee -a /boot/mute_log > /dev/null

	#### Finalize			####################

	echo ''
	echo " 6 - Finalize - Clean up the sources and this script" | sudo tee -a /boot/mute_log
	echo " Finalizing Install..."

	sudo sed -i -e "s/ver.*/ver.${VER}/" ./motd && sudo cp ./motd /etc/motd
    echo " Finalizing Install... Done" | sudo tee -a /boot/mute_log > /dev/null

	echo ' Fixing alsa-state daemon...'
	 sudo systemctl stop alsa-state.service
	 sudo cp ./alsa-state.service /lib/systemd/system/alsa-state.service
	 wait
	 sudo systemctl daemon-reload
	 wait
	 sudo systemctl start alsa-state.service
    echo " Fixing alsa-state daemon... Done" | sudo tee -a /boot/mute_log > /dev/null

	echo ' Turned off the on-board Audio (Headphone).'
	 sudo sed -i -e "s/dtparam=audio=on/#dtparam=audio=on/" /boot/config.txt
	 wait
    echo " Turned off the on-board Audio (Headphone)... Done" | sudo tee -a /boot/mute_log > /dev/null

	echo ' Turned off the HDMI port.'
	 sudo sed -i -e "s/dtoverlay=vc4-kms-v3d/#dtoverlay=vc4-kms-v3d/" -e "s/max_framebuffers=2/#max_framebuffers=2/" /boot/config.txt
	 wait
    echo " Turned off the HDMI port... Done" | sudo tee -a /boot/mute_log > /dev/null

    sudo rm -Rf ../mute_setting
    wait
    echo " Removed mute_setting files." | sudo tee -a /boot/mute_log

	echo ''
    echo " [ mute ] is installed successfully, automatically reboots."
    echo " To control [ mute ], access \" ${hostname}.local \" via web browser from your PC/Tablet after rebooting."
    echo ''

    DATE=$(date)
	echo ' --------  mute install Finished.${DATE} --------' | sudo tee -a /boot/mute_log > /dev/null

	echo ' Rebooting...'
	echo ''

	sudo reboot
fi

exit 0
