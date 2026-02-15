#!/bin/bash

# DBrescanning.cgi
# (C)2025 kitamura_design <kitamura_design@me.com> #

#HTML
cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>

  <head>
    <link rel="stylesheet" type="text/css" href="/css/main.css">
    <script>

     function uiLock(){
       target = parent.document.getElementById("sidebar");
       if (target != null){
          target.className = "sidebar-ui-lock";
       }
     }

     function uiUnlock(){
       target = parent.document.getElementById("sidebar");
       if (target != null){
          target.className = "sidebar-ui-unlock";
       }
     }

	// Set Update notification badge Off
     function setUpdateBadgeOff() {
        target = parent.document.querySelector('#UpdateBadge');
        target.style.display = 'none';
     }

    </script>
   </head>

   <body onload="uiLock()" onunload="uiUnlock(); setUpdateBadgeOff();">

     <div id="loading-top2">
       <div class="loader">
          <div class="loadingtext">Rescanning DB ...</div>
          <div class="progress-bar-base">
          <div class="progress-value-progress"></div>
       </div>
       <h4 id="SSE-CONTENT" class="loadingtext" style="white-space: nowrap;"></h4>
     </div>

     <script>
     const aptUpdateSource = new EventSource('/cgi-bin/MPD/DB_rescan.cgi');

     aptUpdateSource.onmessage = (e) => {
         const content = document.querySelector('#SSE-CONTENT');
         content.textContent = e.data;
     };

     aptUpdateSource.addEventListener('close', (e) => {
         aptUpdateSource.close();
         window.location.href = "/cgi-bin/MPD/MPD.cgi";
     });

    </script>

   </body>
</html>
HTML

exit 0
