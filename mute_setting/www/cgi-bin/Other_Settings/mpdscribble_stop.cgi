#!/bin/bash

# mpdscribble_stop.cgi							 #
# ©2022 kitamura_design <kitamura_design@me.com> #

#mpdscribble stop
	sudo systemctl stop mpdscribble &
	wait

# Go back to page
echo "Location: /cgi-bin/Other_Settings/other_setting_host.cgi"
echo ""
