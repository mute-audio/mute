#!/bin/bash

# Checking.cgi : Call Update Tab menu              #
# (C)2024 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>

  <head>
     <link rel="stylesheet" type="text/css" href="/css/main.css">
     <meta http-equiv="refresh" content="0; ${QUERY_STRING}">
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
    </script>
  </head>

  <body onload="uiLock()" onunload="uiUnlock()">
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Checking Update ...</div>
        <div class="progress-bar-base">
        <div class="progress-value-progress"></div>
        </div>
     </div>
   </div>
  </body>

</html>
HTML
