#!/bin/bash

# MPD_install.cgi                                  #
# (C)2022 kitamura_design <kitamura_design@me.com> #

PKG=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | sed -e 's/+/\ /g' | nkf -Ww --url-input)
query=$(date +%Y%m%d%I%M%S)
RELEASE=$(lsb_release -sc)

# sudo apt update -qq 2>/dev/null 1>/dev/null
# sudo apt clean 2>/dev/null 1>/dev/null
# sudo apt autoremove -y -q 2>/dev/null 1>/dev/null

if [ "$PKG" = "Debian Official ( Stable version )" ]; then

        # install Debian Official
	sudo apt -o Acquire::Retries=5 install -y --no-install-recommends mpd 2>/dev/null 1>/dev/null

	if [ $? != 0 ]; then
	        echo "Location: /cgi-bin/MPD/MPD_install_error.cgi?${QUERY_STRING}"
        	echo ''
	exit 1
	fi

        ## MPD install check
        ## If the mpd installation status is [installed,local],
        ## reinstall mpd so that automatic updates are enabled.

        mpd_Install_CHK=$(sudo apt -a -qq list mpd 2>/dev/null | grep --only-matching "installed,local")

        if [ -n "$mpd_Install_CHK" ]; then
            sudo apt install --reinstall -y mpd 2>/dev/null
        fi

        # replace original mpd.conf to mute mpd.conf
        sudo cp /etc/mpd.conf /var/www/cgi-bin/etc/mpd.conf.bkup
        sudo chmod 755 /var/www/cgi-bin/etc/mpd.conf.bkup
        sudo cp /var/www/cgi-bin/etc/mpd.conf.mute /etc/mpd.conf

	set +e

	# Check NAS already mounted or not
        NAS_count=$(df -ah | grep /mnt.* | wc -l) # Check Multiple NAS Mounted

        if [ $NAS_count != 0 ]; then

            for ((i=1; i<=$NAS_count; i++)); do

              NAS=$(df -ah | grep /mnt.* | cut -d " " -f 1 | sed -n "$i"p) ## Get NAS Volume
              NAS_Dir=$(df -ah | grep --only-matching /mnt.* | cut -d "/" -f 3 | sed -n "$i"p) ##Get NAS Mount Point

              sudo chown mpd:audio /mnt/${NAS_Dir}                      # Ownership to be changed to mpd/audio from root/root
              sudo ln -s /mnt/${NAS_Dir} /var/lib/mpd/music/${NAS_Dir}  # Make link to mpd music dir.

            done
        fi

	sudo ln -s /media /var/lib/mpd/music/USB	    # Make link of /media(USBs) to mpd music dir.
	sudo ln -s /var/lib/mpd/music /var/www/html/        # Make link of mpd music dir to html root for Coverart search.

	set -e

	sudo systemctl enable mpd
        sudo systemctl restart mpd
	sudo apt -o Acquire::Retries=3 install -y --no-install-recommends mpc mpdscribble 2>/dev/null 1>/dev/null
	sudo systemctl stop mpdscribble

        set +e

	sudo systemctl stop mpd.service
	sudo systemctl stop mpd.socket
	sudo systemctl disable mpd.socket
	sudo systemctl start mpd.service

	sudo sed -i -e "s/^pkg=.*/pkg=Debian Stable/" /var/www/cgi-bin/etc/mute.conf

        mpd -V | sudo tee /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt > /dev/null

	sudo cp /var/log/apt/term.log /var/www/cgi-bin/log/install.log

        sudo apt clean 2>/dev/null 1>/dev/null
        sudo apt autoremove -y -q 2>/dev/null 1>/dev/null

        echo "Location: /cgi-bin/MPD/DBupdating.cgi?${query}"
        echo ""

elif  [ "$PKG" = "MPD Official ( Backports version )" ]; then

        ## install MPD Backports
        ## get repo pgp-key
          sudo wget -O /usr/share/keyrings/deb.kaliko.me.gpg https://media.kaliko.me/kaliko.gpg

        ## OS bit check
          OS_bit=$(uname -m)

                if [ "${OS_bit}" = "aarch64" ]; then
                        sudo echo "deb [signed-by=/usr/share/keyrings/deb.kaliko.me.gpg] https://deb.kaliko.me/debian-backports/ ${RELEASE}-backports main" | sudo tee /etc/apt/sources.list.d/deb.kaliko.me.list > /dev/null
                else
                        sudo echo "deb [signed-by=/usr/share/keyrings/deb.kaliko.me.gpg] https://deb.kaliko.me/raspios-backports/ ${RELEASE}-backports main" | sudo tee /etc/apt/sources.list.d/deb.kaliko.me.list > /dev/null
                fi

	sudo apt update -q 2>/dev/null 1>/dev/null

	sudo apt -o Acquire::Retries=5 install -y --no-install-recommends mpd/${RELEASE}-backports  2>/dev/null 1>/dev/null

        if [ $? != 0 ]; then
	        echo "Location: /cgi-bin/MPD/MPD_install_error.cgi?${QUERY_STRING}"
	        echo ''
        exit 1
        fi

        ## MPD install check
        ## If the mpd installation status is [installed,local],
        ## reinstall mpd so that automatic updates are enabled.

        mpd_Install_CHK=$(sudo apt -a -qq list mpd 2>/dev/null | grep --only-matching "installed,local")

        if [ -n "$mpd_Install_CHK" ]; then
            sudo apt install --reinstall -y mpd/${RELEASE}-backports 2>/dev/null 1>/dev/null
        fi

        #replace original mpd.conf to mute mpd.conf
        sudo cp /etc/mpd.conf /var/www/cgi-bin/etc/mpd.conf.bkup
        sudo chmod 755 /var/www/cgi-bin/etc/mpd.conf.bkup
        sudo cp /var/www/cgi-bin/etc/mpd.conf.mute /etc/mpd.conf

        set +e

        # Check NAS already mounted or not
        NAS_count=$(df -ah | grep /mnt.* | wc -l) # Check Multiple NAS Mounted

        if [ $NAS_count != 0 ]; then

            for ((i=1; i<=$NAS_count; i++)); do

              NAS=$(df -ah | grep /mnt.* | cut -d " " -f 1 | sed -n "$i"p) ## Get NAS Volume
              NAS_Dir=$(df -ah | grep --only-matching /mnt.* | cut -d "/" -f 3 | sed -n "$i"p) ##Get NAS Mount Point

              sudo chown mpd:audio /mnt/${NAS_Dir}                      # Ownership to be changed to mpd/audio from root/root
              sudo ln -s /mnt/${NAS_Dir} /var/lib/mpd/music/${NAS_Dir}  # Make link to mpd music dir.

            done
        fi

	sudo ln -s /media /var/lib/mpd/music/USB            # Make link of /media(USBs) to mpd music dir.
        sudo ln -s /var/lib/mpd/music /var/www/html/	    # Make link of mpd music dir to html root for Coverart search.

        set -e

        sudo systemctl enable mpd
        sudo systemctl restart mpd

	sudo apt -o Acquire::Retries=3 install -y --no-install-recommends mpc mpdscribble  2>/dev/null 1>/dev/null

	sudo systemctl stop mpdscribble

	set +e

        sudo systemctl stop mpd.service
        sudo systemctl stop mpd.socket
        sudo systemctl disable mpd.socket
        sudo systemctl start mpd.service

        sudo sed -i -e "s/^pkg=.*/pkg=MPD Backports/" /var/www/cgi-bin/etc/mute.conf

        mpd -V | sudo tee /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt > /dev/null

        sudo cp /var/log/apt/term.log /var/www/cgi-bin/log/install.log

        sudo apt clean 2>/dev/null 1>/dev/null
        sudo apt autoremove -y -q 2>/dev/null 1>/dev/null

        echo "Location: /cgi-bin/MPD/DBupdating.cgi?${query}"
        echo ''

else
	echo "Location: /cgi-bin/MPD/check_MPD.cgi?${query}"
	echo ''

fi
