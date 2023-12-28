#!/bin/bash

# mpdscribble_restart.cgi						   #
# (C)2022 kitamura_design <kitamura_design@me.com> #


# mpdscribble restart
	sudo systemctl restart mpdscribble 2>/dev/null 1>/dev/null

	enable_CHECK=$(systemctl is-enabled mpdscribble)

	if [ "$enable_CHECK" = "disabled" ]; then
	sudo systemctl enable mpdscribble 2>/dev/null 1>/dev/null
    fi
	
# Goback to page
echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Other_Settings/Other_setting.cgi"
echo ""
