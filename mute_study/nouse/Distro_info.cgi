#!/bin/bash

#Distro_info.cgi
#kitamura_design

#Get the  informations in advance

	#(Nothing)

#HTML

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"

echo "<html>"
echo 	"<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo 	"</head>"

echo "<body>"
	#Distro_info
echo	"<h1>RaspberryPi OS</h1>"
echo	"<h3>Distribution : "
echo	"$(lsb_release -a | sed -n 2p | cut -d ":" -f 2)"
echo    "<a href=\"/cgi-bin/reboot.cgi\" target=\"_self\" class=\"button reboot\">Reboot</a>"
echo	"</h3>"

echo    "<h4>Status:</h4>"
echo    "<code>$(uname -a)</code>"
echo    "<br>"
echo    "<code>$(cat /etc/rpi-issue)</code>"

echo "</body>"
echo "</html>"
