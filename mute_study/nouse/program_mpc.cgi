#!/bin/bash

#program_mpc.cgi
#kitamura_design

#Get infomations
	#Nothing

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo  "</head>"

echo "<body>"

        #mpc
echo	"<h1>Music Database</h1>"
echo    "<h3>Database Info."
echo    "<a href=\"/cgi-bin/mpc_list_album.cgi\" target=\"mainview\" class=\"button mpc_album\">Album List</a>"
echo    "</h3>"

echo    "<code>"
echo    "$(mpc help | sed -n 2p)<br>"
echo	"$(mpc stats)"
echo    "</code>"

echo "</body>"
echo "</html>"
