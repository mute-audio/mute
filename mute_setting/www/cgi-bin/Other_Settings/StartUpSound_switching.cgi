#!/bin/bash

# StartUpSound_switching.cgi                       #
# (C)2023 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

#HTML
echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css\">"
echo    "<meta http-equiv=\"refresh\" content=\"0; URL=/cgi-bin/Other_Settings/StartUpSound_sw.cgi?${QUERY_STRING}\">"
echo  "</head>"

echo "<body>"

#### Loading Screen
   cat <<HTML
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Switching Startup Sound ...</div>
        <!-- progress class="loading"></progress -->
     </div>
   </div>
HTML

echo "</body>"
echo "</html>"
