#!/bin/bash

#VER=$(uname -r)
#ls /lib/modules/${VER}/kernel/sound/soc/bcm | cut -d '-' -f 3,4,5 | cut -d '.' -f 1 > /var/www/cgi-bin/dac_list/dac_list.txt
cat /var/www/cgi-bin/dac_list/dac_list.txt | sed -e 's/^/<option value=\"dtoverlay=/g' -e 's/$/\">/g' > /var/www/cgi-bin/dac_list/dac_option.txt
cat /var/www/cgi-bin/dac_list/dac_list.txt | sed -e 's/$/<\/option>/g' > /var/www/cgi-bin/dac_list/dac_title.txt

echo "Content-type: text/html; charset=utf-8"
echo

echo "<!DOCUTYPE html>"
echo "<html>"

echo  "<head>"
echo    "<link rel=\"stylesheet\" type=\"text/css\" href=\"/pureMPD.css\">"
echo  "</head>"

echo "<body>"

echo  "<p>"
echo   "<select  name=\"dac_list\">"
echo   "$(paste -d'.' /var/www/cgi-bin/dac_list/dac_option.txt /var/www/cgi-bin/dac_list/dac_title.txt)"
echo   "</select>"
echo  "</p>"

echo "</body>"
echo "</html>"
