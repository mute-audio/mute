#!/bin/bash

set -e

## [ mute ] Packager shell
## (C)2022 kitamura_design <kitamura_design@me.com>

## Show Title
    echo ""
    echo " [ mute ] Packager"
    echo ""

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
    VER=$(cat ./mute_setting/www/cgi-bin/etc/mute.conf | grep ver= | sed -e 's/[^0-9]//g')

    echo -n " Packaging of \" mute_update_$VER.zip \" ..."

    sudo rm -r ./mute_update/www
    sudo cp -R ./mute_setting/www/ ./mute_update/www
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