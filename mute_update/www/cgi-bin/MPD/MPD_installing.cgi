#!/bin/bash

# MPD_installing.cgi
# (C)2026 kitamura_design <kitamura_design@me.com> #

PKG=$(echo ${QUERY_STRING} | cut -d '=' -f 2 | sed -e 's/+/\ /g' | nkf -Ww --url-input)

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

echo    "</script>"
echo  "</head>"

echo "<body onLoad=\"uiLock()\" onunload=\"uiUnlock()\">"

#### Loading Screen
   cat <<HTML
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Installing MPD : [ ${PKG} ] ...</div>
        <div class="progress-bar-base">
        <div class="progress-value-progress"></div>
        </div>
       <h4 id="SSE-CONTENT" class="loadingtext" style="white-space: nowrap;"></h4>
     </div>
   </div>

   <script>
     const mpdInstallSource = new EventSource('/cgi-bin/MPD/MPD_install.cgi?${QUERY_STRING}');

     mpdInstallSource.onmessage = (e) => {
         const content = document.querySelector('#SSE-CONTENT');
         content.textContent = e.data;
     };

     mpdInstallSource.addEventListener('close', (e) => {
         mpdInstallSource.close();
         window.location.href = "/cgi-bin/MPD/check_MPD.cgi";
     });

   </script>
HTML

echo "</body>"
echo "</html>"
