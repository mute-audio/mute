#!/bin/bash

## [ mute ] DAC list generator shell
## (C)2022 kitamura_design <kitamura_design@me.com>


## Extract the Info line containing "audio", "sound", "music", "DAC", 
## and "amplifier" from /boot/overlays/README and store it in the $INFO.

INFO=$(sudo grep -i -e audio -e sound -e music -e amplifier -e DAC /boot/overlays/README | grep "Info")

## Firstly using $INFO, extract the four lines below the Info line from /boot/overlays/README.
## Next, extract the "Info" and "Load" lines AGAIN, 
## insert carriage returns to make them easier to read, 
## and clean up unnecessary characters, symbols, and spaces.

sudo grep -A4 "$INFO" /boot/overlays/README \
| grep -e "Info" -e "Load" \
| sed "/Load/a \ " \
| sed -e "s/Configures //g" -e "s/the //g" -e "s/:   /:/g" -e "/Load/s/,<param>//g" -e "/Load/s/=<val>//g" -e "/Info/s/\.$//g" \
| sudo tee ./dac_list.txt.source 2>/dev/null
