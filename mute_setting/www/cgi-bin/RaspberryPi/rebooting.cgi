#!/bin/bash

# rebooting.cgi                                    #
# (C)2023 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo ""

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

#### Loading Screen
   cat <<HTML
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Rebooting ...</div>
        <div class="progress-bar-base">
        <div class="progress-value-progress"></div>
        </div>
     </div>
   </div>
HTML

## Auto-reconnect after rebooting
cat <<HTML
<script>

// Set Reboot notification badge Off
function setRebootBadgeOff() {
   target = parent.document.querySelector('#RaspberrypiBadge');
   target.style.display = 'none';
}

setRebootBadgeOff();

// Kick Reboot process
function rebootMute() {
  fetch( '/cgi-bin/RaspberryPi/reboot.cgi' )
  .then( response => {
   if(!response.ok){
      return;
   }
  })
  .catch((error) => console.log(error))
}

rebootMute();

// Wait for Reboot done
setInterval( autoReconnect , 10000);

function autoReconnect() {
  fetch("/")
  .then(response => {
   if(response.ok){
      parent.location.href="/cgi-bin/index.cgi";
    }else{
      return;
    }
  })
  .catch((error) => console.log(error))
}

</script>
HTML

echo "</body>"
echo "</html>"
