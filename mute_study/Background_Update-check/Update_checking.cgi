#!/bin/bash

# Updae_checking.cgi
# (C)2022 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css?$query\">"
echo    "<meta http-equiv=\"refresh\" content=\"0; URL=/cgi-bin/Update/Update_Checker.cgi\">"
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

echo "<body onload=\"uiLock()\" onunload=\"uiUnlock()\">"

   cat <<HTML
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext"> Checking Update ... </div>
        <progress class="progress"></progress>
     </div>
   </div>
HTML

echo "</body>"
echo "</html>"
