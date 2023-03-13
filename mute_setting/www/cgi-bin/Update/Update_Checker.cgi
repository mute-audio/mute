#! /bin/bash

stsUPD=$(sudo apt update -qq 2>/dev/null | cut -d"." -f 1)
apt_list=$(sudo apt list --upgradable -qq 2>/dev/null | sed -e "s/$/<br>/g")

if [ "$stsUPD" != "All packages are up to date" ]; then

        echo "${stsUPD}." | sudo tee /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "<br>" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt > /dev/null
        echo "$apt_list" | sudo tee -a /var/www/cgi-bin/Update/Update_notice.txt # > /dev/null

        echo "Location: /cgi-bin/Update/Update.cgi"
        echo ''
else
        echo "${stsUPD}." | sudo tee /var/www/cgi-bin/Update/Update_notice.txt > /dev/null

        echo "Location: /cgi-bin/Update/Update.cgi"
        echo ''

fi

exit 0