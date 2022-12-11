#!/bin/bash

# host_pwd_change_processing.cgi	               #
# (C)2022 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css?$query\">"
echo    "<meta http-equiv=\"refresh\" content=\"0; URL=/cgi-bin/RaspberryPi/host_pwd_change.cgi?${QUERY_STRING}\">"
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

#echo "<p>${QUERY_STRING}</p>"

#### Loading Screen
echo "<div id=\"loading-top2\">"

######### Loading Animation
echo   "<div class=\"loader\">"
echo      "<div class=\"ball-scale-ripple\">"
echo        "<div></div>"
echo      "</div>"
echo     "<div class=\"loadingtext\">Setting Password ...</div>"
echo   "</div>"
######### Loading Animation

echo "</div>"
#### Loading Screen

echo "</body>"
echo "</html>"
