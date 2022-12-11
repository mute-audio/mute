#!/bin/bash

echo "Content-type: text/html; charset=UTF-8"
echo

title="$(mpc -f %title% current)"

echo "<!DOCUTYPE html>"
echo "<html>"
echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo  "</head>"
echo    "<body>"
echo            "<div class=\"nowplaying\">"
echo            "<h3>${title:- -- Stopped --}</h3>" #Title
echo            "<p>$(mpc -f %artist% current)</p>" #Artist
echo            "<p>$(mpc -f %album% current)</p>" #Album
echo            "<p>$(mpc -f %name% current)</p>" #Webradio(name)
echo            "<p>$(mpc -f %time% current)</p>" #Time
echo            "</div>"

echo "</body>"
echo "</html>"
