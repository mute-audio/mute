#!/bin/bash

## mute_packager.sh
## [ mute ] Packager shell
## (C)2024 kitamura_design <kitamura_design@me.com>

## Input error handling
if [ $# != 1 ] ; then

cat <<EOL
Usage:./mute_packager.sh [VERSION]
e.g. "./mute_packager.sh 1.0.9-beta"
EOL

exit 1
fi

set -e

## Show Title
    echo ""
    echo " [ mute ] Packager Ver.${1} "
    echo ""

## Pre-cooking: Rewrite Version @mute.conf
    sudo sed -i "" -e "s/ver=.*/ver=${1}/" ./mute_setting/www/cgi-bin/etc/mute.conf 2>/dev/null 1>/dev/null

## Change Permission
    echo -n " Change permission of source dir ..."
    sudo chmod -R 755 ./mute_setting/www
    echo " Done."

## Make mute_setting_yymmdd.zip
    TimeStamp=$(date +%y%m%d)

    echo -n " Packaging of \" mute_setting_$TimeStamp.zip \" ..."

    sudo zip -rq ./packages/mute_setting_$TimeStamp.zip ./mute_setting

    echo " Done."

## Copy www to mute_update/www, and then Make mute_update_VER.zip
    # Extract version number from input
    VER=$(echo $1 | sed -e 's/[^0-9]//g')

    echo -n " Packaging of \" mute_update_$VER.zip \" ..."

## Rewrite update.info
    sudo sed -i "" -e "s/ver=.*/ver=${1}/" ./mute_update/update.info

## Rewrite package.info
    sudo sed -i "" -e "s/ver=.*/ver=${1}/" ./packages/package.info

## Replace the Source
    sudo rm -r ./mute_update/www
    sudo cp -R ./mute_setting/www/ ./mute_update/www

## Make Zip Package
    sudo zip -rq ./packages/mute_update_$VER.zip ./mute_update

    echo " Done."

## Reset Permission
    echo -n " Reset permission of source dir ..."

    sudo chmod -R 777 ./mute_setting/www

    echo " Done."
    echo ""
    echo " The process completed successfully."
    echo ""

exit 0