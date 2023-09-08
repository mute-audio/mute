#!/bin/bash

## mpdscribble_stop.cgi
## (C)2022 kitamura_design <kitamura_design@me.com>

## mpdscribble stop
	sudo systemctl stop mpdscribble &
	wait

## Go back to page
echo "Location: /cgi-bin/loading.cgi?/cgi-bin/Other_Settings/Other_setting.cgi"
echo ""
