#!/bin/bash

# MPD_not_installed.cgi                 		   #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Get infomations

query=$(date +%Y%m%d%I%M%S)

#### HTML
echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/css/main.css?$query\">"

echo  "<script>"

echo    "function keepHover(){"
echo      "target = parent.document.getElementById(\"MPD\");"
echo      "if (target != null){"
echo         "target.className = \"menutab-keephover\";"
echo      "}"
echo    "}"

echo    "function offHover(){"
echo      "target = parent.document.getElementById(\"MPD\");"
echo      "if (target != null){"
echo         "target.className = \"menutab\";"
echo      "}"
echo    "}"

echo  "</script>"

echo  "</head>"

echo "<body id=\"iframe\" onLoad=\"keepHover()\" onunload=\"offHover()\">"

######## MPD

OS_bit=$(uname -m)

echo    "<h1>MPD</h1>"

echo    "<h3>Music Player Deamon <div class=\"status\">Not Installed</div> </h3>"

if [ "${OS_bit}" = "aarch64" ]; then

echo    "<form method=GET action=\"/cgi-bin/MPD/MPD_install_processing.cgi\" target=\"_self\">"
echo        "<div class=\"setting-items-wrap\">"
echo          "<input id=\"Apply\" type=\"submit\" value=\"Install \" class=\"button\">"
echo          "<div class=\"ellipsis-wrap\"><div class=\"allow-down\"></div></div>"
echo          "<select  id=\"package\" name=\"package\" class=\"inputbox-single\">"
echo            "<option selected>Debian Official ( Stable version )</option>"
echo            "<option disabled>MPD Official ( Backports version )</option>"
echo          "</select>"
echo          "<label for=\"\">Package</label>"
echo        "</div>"
echo    "</form>"

else

echo    "<form method=GET action=\"/cgi-bin/MPD/MPD_install_processing.cgi\" target=\"_self\">"
echo        "<div class=\"setting-items-wrap\">"
echo          "<input id=\"Apply\" type=\"submit\" value=\"Install \" class=\"button\">"
echo          "<div class=\"ellipsis-wrap\"><div class=\"allow-down\"></div></div>"
echo          "<select  id=\"package\" name=\"package\" class=\"inputbox-single\">"
echo            "<option selected>Debian Official ( Stable version )</option>"
echo            "<option>MPD Official ( Backports version )</option>"
echo          "</select>"
echo          "<label for=\"\">Package</label>"
echo        "</div>"
echo    "</form>"

fi

echo   "<div class=\"separator\">"
echo     "<hr>"
echo   "</div>"

echo    "<br>"
echo    "<p class=\"bodytext2\">"
echo    "MPD is not yet installed, so you will first need to select and install the MPD package."
echo    "Choose the MPD package and install it; \"an official\" Debian version or an \"unofficial\" Backports version by the MPD project."
echo    "<br>"
echo    "CAUTION: Backports version supports ONLY 32-bit OS."
echo    "<br>"
echo    "</p>"

echo "</body>"
echo "</html>"
