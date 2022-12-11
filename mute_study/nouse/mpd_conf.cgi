#!/bin/bash

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/main.css\">"
echo "</head>"

echo "<body>"

#echo "<h1>MPD</h1>"
        #MPD Conf.
echo    "<div class=\"title-btn-title\">"
#echo      "<a href=\"/cgi-bin/MPD.cgi\" class=\"button\">Done</a>"
echo	  "<h3>MPD.conf</h3>"
echo    "</div>"

echo	"<h4>"
echo	"$(cat /etc/mpd.conf)"
echo	"</h4>"

echo "</body>"
echo "</html>"
