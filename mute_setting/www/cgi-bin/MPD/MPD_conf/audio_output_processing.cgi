#!/bin/bash

# audio_output_processing.cgi                    #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Clean QUERY_STRING
 OPTION=$(echo ${QUERY_STRING} | cut -d '=' -f 1 | nkf -Ww --url-input)

query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css?$query\">"
echo    "<meta http-equiv=\"refresh\" content=\"0; /cgi-bin/MPD/MPD_conf/audio_output_$OPTION.cgi?${QUERY_STRING}\">"
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
        <div class="loadingtext">Setting Audio Output ...</div>
        <div class="progress-bar-base">
        <div class="progress-value-loading"></div>
        </div>
     </div>
   </div>
HTML

echo "</body>"
echo "</html>"
