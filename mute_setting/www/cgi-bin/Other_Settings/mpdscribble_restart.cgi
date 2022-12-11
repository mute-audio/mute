#!/bin/bash

# mpdscribble_restart.cgi						   #
# (C)2022 kitamura_design <kitamura_design@me.com> #


# mpdscribble restart
	sudo systemctl restart mpdscribble &
	wait

# Goback to page
echo "Location: /cgi-bin/Other_Settings/other_setting_host.cgi"
echo ""
