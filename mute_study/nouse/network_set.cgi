#!/bin/bash

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/main.css\">"
echo "</head>"

echo "<body>"

echo "<h1>Network Info.</h1>"
        #NetworSetting
echo    "<h4>Network Setting<a href=\"/cgi-bin/Host_info.cgi\" class=\"button backtotop\">Done</a></h4>"

echo    "<p>"
echo    "<code>"
echo    "$(ifconfig -v)"
echo    "</code>"
echo    "</p>"

echo "</body>"
echo "</html>"


