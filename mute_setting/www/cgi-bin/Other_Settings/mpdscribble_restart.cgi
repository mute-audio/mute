#!/bin/bash

# mpdscribble_restart.cgi						   #
# (C)2022 kitamura_design <kitamura_design@me.com> #


# mpdscribble restart
	sudo systemctl restart mpdscribble &
	wait

# Goback to page
echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Other_Settings/Other_setting.cgi"
echo ""
