#!/bin/bash

# MPD_install_processing.cgi                	   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

PKG=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | sed -e 's/+/\ /g' | nkf -Ww --url-input)
query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css?$query\">"
echo    "<meta http-equiv=\"refresh\" content=\"0; URL=/cgi-bin/MPD/MPD_install.cgi?${QUERY_STRING}\">"
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
        <div class="loadingtext">Installing MPD : [ ${PKG} ] ...</div>
        <div class="loadingtext">It may take quite a while (around 10 -15 minutes, depends on environment). Please wait.</div>
        <progress class="progress"></progress>
     </div>
   </div>
HTML

echo "</body>"
echo "</html>"
