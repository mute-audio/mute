#!/bin/bash

# Update_mute_error.cgi		                     #
# (C)2022 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#HTML

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css?$query\">"
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

######## Error Msg.
echo   "<div id=\"loading-top2\">"
echo     "<div class=\"loadingtext\"> ...Some Error occurred during Update [ mute ]. </div>"
echo     "<a href=\"/cgi-bin/loading.cgi?/cgi-bin/RaspberryPi/Raspberrypi.cgi\" target=\"_self\" class=\"button2\"> Cancel </a>"
echo     "<a href=\"/cgi-bin/Checking.cgi?/cgi-bin/Update/Update.cgi\" target=\"_self\" class=\"button\"> Retry </a>"
echo   "</div>"

echo "</body>"
echo "</html>"
