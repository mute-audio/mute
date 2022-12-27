#!/bin/bash

volume="$(mpc -f %file% current | cut -d / -f 1)"
folder1="$(mpc -f %file% current | cut -d / -f 2)"
folder2="$(mpc -f %file% current | cut -d / -f 3)"

if [ "$volume" = "http:" ]; then
  cover="$(echo /image/default_cover.png)"

  elif [ -z "$volume" ]; then
  cover="$(echo /image/default_cover.png)"

  else
  cover="$(echo /music/${volume}/${folder1}/${folder2}/Cover.jpg)"
fi

title="$(mpc -f %title% current)"

query=$(date +%Y%m%d%I%M%S)

#HTML
cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<meta http-equiv="Refresh" content="60">
  <link rel="stylesheet" type="text/css" href="/css/main.css?$query">
  </head>

  <body>
   <img src="${cover}" class="cover">
   <h2>${title:- -- Stopped --}</h2>
   <div class="songinfo">
     <p>$(mpc -f %artist% current)</p>
     <p>$(mpc -f %album% current)</p>
     <p>$(mpc -f %name% current)</p>
     <p>$(mpc -f %time% current)</p>
   </div>
  </body>
</html>
HTML
