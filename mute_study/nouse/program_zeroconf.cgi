#!/bin/bash

#program_zeroconf.cgi
#kitamura_design

#Get infomations:Nothing

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo  "<head>"

echo "<body>"

	#Zeroconf (Avahi)
echo    "<h3>ZeroConf (Bonjour) :"
echo    "$(avahi-daemon --version | head -n1 | sed -e 'a\<br>')"
echo    "</h3>"
echo    "<br>"
echo    "<code>$(systemctl status avahi-daemon | head -n3)"
echo    "</code>"

echo "</body>"
echo "</html>"
