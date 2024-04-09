#!/bin/bash

# Updating_mute.cgi
# (C)2024 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#HTML
cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
<head>
   <link rel="stylesheet" type="text/css" href="/css/main.css">
   <meta http-equiv="refresh" content="0; URL=/cgi-bin/Update/Update_mute_exec.cgi">
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
<body onLoad="uiLock()" onunload="uiUnlock(); setUpdateBadgeOff();">

<!-- Loading Screen -->
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Updating [ mute ] ...</div>
        <div class="progress-bar-base">
        <div class="progress-value-progress"></div>
        </div>
     </div>
   </div>

</body>
</html>
HTML

exit 0