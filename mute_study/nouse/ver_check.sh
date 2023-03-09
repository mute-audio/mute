#!/bin/bash

ver_UPDATE=$(\
sudo wget --no-check-certificate -q -O - \
"https://www.dropbox.com/s/9op8f7ras6s4a94/mute.conf" | \
grep "ver=" | \
sed -e 's/[^0-9]//g'\
)

ver_CURRENT=$(\
grep "ver=" /var/www/cgi-bin/etc/mute.conf | \
sed -e 's/[^0-9]//g'\
)

if [[ "$ver_UPDATE" -gt "$ver_CURRENT" ]]; then

	echo "[ mute ] Update available."
else

	echo "[ mute ] is up to date."
fi

exit 0
