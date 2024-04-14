#!/bin/bash

# dac_applying.cgi		                           #
# (C)2024 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#target DAC
DAC=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | nkf -Ww --url-input)

#HTML

if [ -z "$DAC" ]; then

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

######## Error Msg.
echo   "<div id=\"loading-top2\">"
echo     "<div class=\"loadingtext\"> ...No DAC Selected. Try again. </div>"
echo     "<a href=\"/cgi-bin/Sound_Device/Sound_device.cgi\" target=\"_self\" class=\"toggle-on-sw\"> Retry </a>"
echo   "</div>"

echo "</body>"
echo "</html>"

else

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css\">"
echo    "<meta http-equiv=\"refresh\" content=\"0; URL=/cgi-bin/Sound_Device/i2s_dac_install.cgi?${QUERY_STRING}\">"
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

#### Loading Screen
   cat <<HTML
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Applying DAC ...</div>
        <div class="progress-bar-base">
        <div class="progress-value-loading"></div>
        </div>
     </div>
   </div>
HTML

echo "</body>"
echo "</html>"

fi
