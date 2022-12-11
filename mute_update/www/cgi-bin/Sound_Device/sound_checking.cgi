#!/bin/bash

# SoundChecking.cgi                                #
# (C)2022 kitamura_design <kitamura_design@me.com> #

#Clean QUERY_STRING
 HWno=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css?$query\">"
echo    "<meta http-equiv=\"refresh\" content=\"0; URL=/cgi-bin/Sound_Device/sound_check.cgi?${QUERY_STRING}\">"
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

######## Loading Screen
echo   "<div id=\"loading-top2\">"
echo      "<div class=\"loadingtext\"> Checking Sound on ${HWno}... </div>"
echo      "<a href=\"/cgi-bin/Sound_Device/stop_sp_test.cgi\" target=\"_self\" class=\"toggle-on-sw\"> Stop </a>"
echo   "</div>"

echo "</body>"
echo "</html>"
