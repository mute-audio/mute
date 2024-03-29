#!/bin/bash

# submit_SCRIBBLE.cgi  						 #
# ©2022 kitamura_design <kitamura_design@me.com> #

USER=$(echo ${QUERY_STRING} | cut -d '&' -f 1 | cut -d '=' -f 2 | nkf -Ww --url-input)
PASS=$(echo ${QUERY_STRING} | cut -d '&' -f 2 | cut -d '=' -f 2 | nkf -Ww --url-input)

#Check Status @ [last.fm] part
URL=$(sudo sed -n -e '/\[last.fm\]/,+3p' /etc/mpdscribble.conf | sed -n -e 2P)
CurrentUSER=$(sudo sed -n -e '/\[last.fm\]/,+3p' /etc/mpdscribble.conf | sed -n -e 3P)
CurrentPWD=$(sudo sed -n -e '/\[last.fm\]/,+3p' /etc/mpdscribble.conf | sed -n -e 4P)

	sudo systemctl stop  mpdscribble

	sudo sed -i -e 's/#\[last.fm\]/\[last.fm\]/' /etc/mpdscribble.conf
	sudo sed -i -e 's/#url\ \=\ http\:\/\/post.audioscrobbler.com\//url\ \=\ http\:\/\/post.audioscrobbler.com\//g' /etc/mpdscribble.conf
	sudo sed -i -e "s/${CurrentUSER}/username\ \=\ ${USER}/" /etc/mpdscribble.conf
	sudo sed -i -e "s/${CurrentPWD}/password\ \=\ ${PASS}/" /etc/mpdscribble.conf

	sudo systemctl restart mpdscribble

	enable_CHECK=$(systemctl is-enabled mpdscribble)

	if [ "$enable_CHECK" = "disabled" ]; then
	sudo systemctl enable mpdscribble 2>/dev/null 1>/dev/null
    fi

    echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Other_Settings/Other_setting.cgi"
    echo ""
