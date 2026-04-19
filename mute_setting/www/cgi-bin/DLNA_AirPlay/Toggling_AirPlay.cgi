#!/bin/bash
# Toggling_AirPlay.cgi
# (C)2026 kitamura_design <kitamura_design@me.com>

echo "Content-type: text/html; charset=utf-8"
echo ""

cat <<HTML
<!DOCUTYPE html>
<html>
<head>
    <link rel="stylesheet" type="text/css" href="/css/main.css">
    <script>
        function uiLock(){
            var target = parent.document.getElementById("sidebar");
            if (target != null) { target.className = "sidebar-ui-lock"; }
        }

        function uiUnlock(){
            var target = parent.document.getElementById("sidebar");
            if (target != null) { target.className = "sidebar-ui-unlock"; }
        }

        function runProcess() {
            // Call the execution-only CGI
            fetch('Toggle_AirPlay.cgi')
            .then(response => {
                if(response.ok){
                    // Redirect back to main renderer page
                    location.href = "/cgi-bin/DLNA_AirPlay/DLNA_AirPlay.cgi";
                }
            })
            .catch((error) => {
                console.log(error);
                location.href = "/cgi-bin/DLNA_AirPlay/DLNA_AirPlay.cgi";
            })
        }
    </script>
</head>
<body onLoad="uiLock(); runProcess();" onUnload="uiUnlock()">
    <div id="loading-top2">
        <div class="loader">
            <div class="loadingtext">Updating AirPlay ...</div>
            <div class="progress-bar-base">
                <div class="progress-value-progress"></div>
            </div>
        </div>
    </div>
</body>
</html>
HTML
