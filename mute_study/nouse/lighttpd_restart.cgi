#!/bin/bash

	#lighttpd restart
	sudo systemctl restart lighttpd &
	wait

echo "Location: http://raspberrypi.local/cgi-bin/program_lighttpd.cgi"
echo
