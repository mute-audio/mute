#!/bin/bash
# Renaming_DLNA.cgi
# (C)2026 kitamura_design <kitamura_design@me.com>

# Extract the new name from the form parameter
NEW_NAME=$(echo "$QUERY_STRING" | grep -o 'dlnaNAME=[^&]*' | cut -d'=' -f2)

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

        function runRename() {
            // Call the execution CGI with the new name
            fetch('Rename_DLNA.cgi?dlnaNAME=${NEW_NAME}')
            .then(response => {
                if(response.ok){
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
<body onLoad="uiLock(); runRename();" onUnload="uiUnlock()">
    <div id="loading-top2">
        <div class="loader">
            <div class="loadingtext">Updating DLNA Display Name...</div>
            <div class="progress-bar-base">
                <div class="progress-value-progress"></div>
            </div>
        </div>
    </div>
</body>
</html>
HTML
