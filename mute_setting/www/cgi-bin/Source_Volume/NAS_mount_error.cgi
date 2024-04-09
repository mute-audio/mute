#!/bin/bash

# NAS_mount_error.cgi	                    	   #
# (C)2023 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#HTML

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css\">"
echo    "<script>"

echo    "function uiLock(){"
echo      "target = parent.document.getElementById(\"sidebar\");"
echo      "if (target != null){"
echo         "target.className = \"sidebar-ui-lock\";"
echo      "}"
echo    "}"

echo    "function uiUnlock(){"
echo      "target = parent.document.getElementById(\"sidebar\");"
echo      "if (target != null){"
echo         "target.className = \"sidebar-ui-unlock\";"
echo      "}"
echo    "}"

echo  "</script>"
echo  "</head>"

echo "<body onLoad=\"uiLock()\" onunload=\"uiUnlock()\">"

RaspberryPiMenu="/cgi-bin/RaspberryPi/Raspberrypi.cgi"
SourceVolumeMenu="/cgi-bin/Source_Volume/Source_volume.cgi"

######## Loading Screen
echo   "<div id=\"loading-top2\">"
echo     "<div class=\"loadingtext\"> ...NAS mount failed. </div>"
echo     "<a href=\"/cgi-bin/loading.cgi?${RaspberryPiMenu}\" target=\"_self\" class=\"button2\"> Cancel </a>"
echo     "<a href=\"/cgi-bin/loading.cgi?${SourceVolumeMenu}\" target=\"_self\" class=\"button\"> Retry </a>"
echo   "</div>"

echo "</body>"
echo "</html>"