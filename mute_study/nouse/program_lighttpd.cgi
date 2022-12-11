#!/bin/bash

#Get infomations
	#(nothing)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo  "</head>"

echo "<body>"

	#Lighttpd

echo    "<h1>CoverArt & WebUI</h1>"

echo	"<h3>Internal Web Server : "
echo    "$(lighttpd -V | head -n1)"
echo    "<a href=\"/cgi-bin/lighttpd_restart.cgi\" target=\"_self\" class=\"button\">Restart</a>"
echo    "</h3>"

echo	"<h4>Status:</h4>"
echo	"<code>$(systemctl status lighttpd | head -n3)</code>"

echo    "<p class=\"spacer\"></p>"

echo "</body>"
echo "</html>"
