#!/bin/bash

#Poweroff_process.cgi
#kitamura_design

#Get the  informations in advance

#Getting the Hardware info
mainboard=$(sudo lshw -C system -disable usb -disable scsi -disable network | sed -n 3p | cut -d ":" -f 2)

#HTML

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"
echo 	"<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo	"</head>"

echo "<body>"

	#MainBoard informations
echo	"<h1>Main Board / OS</h1>"

echo    "<div class=\"title-btn\">"
echo      "<div class=\"title-btn-title\">"
echo        "<h3>Main Board : ${mainboard}</h3>"
echo      "</div>"
echo        "<h3><a href=\"\" target=\"_self\" class=\"button\">Poweroff</a></h3>"
echo    "</div>"

echo    "<h4>Status:</h4>"
echo	"<code>$(lscpu)</code>"
echo    "<br><code>CPU Temp:            $(./temp_info2.cgi)</code>"

echo    "<p class=\"spacer\"></p>"

#Distro_info
echo    "<div class=\"title-btn\">"
echo      "<div class=\"title-btn-title\">"
echo	    "<h3>OS : $(lsb_release -a | sed -n 2p | cut -d ":" -f 2)</h3>"
echo      "</div>"
echo        "<h3><a href=\"\" target=\"_self\" class=\"button\">Rebooting...</a></h3>"
echo	"</div>"

echo    "<h4>Status:</h4>"
echo    "<code>$(uname -a)</code>"
echo    "<br>"
echo    "<code>$(cat /etc/rpi-issue)</code>"

echo  "<object data=\"cgi-bin/reboot.cgi\" target=\"_self\">[process unavalable]</object>"
echo "</body>"
echo "</html>"
