#!/bin/bash

echo "Content-type: text/html; charset=utf-8"
echo

volume="$(mpc -f %file% current | cut -d / -f 1)"
folder1="$(mpc -f %file% current | cut -d / -f 2)"
folder2="$(mpc -f %file% current | cut -d / -f 3)"

if [ $volume = nas ]; then

cover="$(echo /music/${volume}/${folder1}/${folder2}/Cover.jpg)"
else
cover="$(echo /default_cover.png)"
fi

title="$(mpc -f %title% current)"

#HTML
echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo	"<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo  "</head>"

echo  "<body>"
echo           "<h1>Now Playing</h1>"
echo		"<img src=\"${cover}\" class=\"cover\">"  #coverart
		#Song Info
echo            "<h2>${title:- -- Stopped --}</h2>" #Title
echo            "<div class=\"songinfo\">"
echo            "<p>$(mpc -f %artist% current)</p>" #Artist
echo            "<p>$(mpc -f %album% current)</p>" #Album
echo            "<p>$(mpc -f %name% current)</p>" #Webradio(name)
echo            "<p>$(mpc -f %time% current)</p>" #Time
echo		"</div>"
echo "</body>"
echo "</html>"

