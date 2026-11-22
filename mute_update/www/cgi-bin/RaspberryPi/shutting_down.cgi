#!/bin/bash

# shutting_down.cgi                                #
# (C)2026 kitamura_design <kitamura_design@me.com> #

# Browser reload after kicked : cancel, back to start page
if [ "${QUERY_STRING}" = "done" ]; then
    echo "Location: /cgi-bin/start.cgi"
    echo ""
    exit 0
fi

query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<!DOCTYPE html>"
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

echo "<div id=\"loading-top2\">"
echo     "<div class=\"loadingtext\">Powered off.</div>"
echo     "<a href=\"/cgi-bin/index.cgi\" target=\"_parent\" class=\"toggle-on-sw\"> Reload </a>"
echo "</div>"

## Auto-reconnect after rebooting
cat <<HTML
<script>

function powerOffMute() {
  fetch( '/cgi-bin/RaspberryPi/poweroff.cgi' )
  .then( response => {
   if(!response.ok){
      return;
   }
  })
  .catch((error) => console.log(error))
}

// Mark this history entry as "already kicked"
history.replaceState(null, "", "/cgi-bin/RaspberryPi/shutting_down.cgi?done");

powerOffMute();

// setInterval( autoReconnect , 10000)

// function autoReconnect() {
// fetch("/")
// .then(response => {
//   if(response.ok){parent.location.href="/index.html"}
// })
// }

</script>
HTML

echo "</body>"
echo "</html>"
