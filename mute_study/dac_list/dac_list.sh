#!/bin/bash

VER=$(uname -r)

mkdir -p /home/pi/dac_list
ls /lib/modules/${VER}/kernel/sound/soc/bcm | cut -d '-' -f 3,4,5 | cut -d '.' -f 1 > /home/pi/dac_list/daclist.txt
