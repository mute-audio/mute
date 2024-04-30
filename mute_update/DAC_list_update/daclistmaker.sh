#!/bin/bash

## [ mute ] DAC list generator shell
## (C)2024 kitamura_design <kitamura_design@me.com>


## Extract the Info line containing "audio", "sound", "music", "DAC", 
## and "amplifier" from /boot/overlays/README and store it in the $INFO.

# Check current OS Codename
OS_codename=$(lsb_release -a |  grep Codename | cut -f 2)

if [ ${OS_codename} = "bookworm" ]; then
   bootDIR="boot/firmware"
else
   bootDIR="boot"
fi

INFO=$(sudo grep -i -e audio -e sound -e music -e amplifier -e DAC /${bootDIR}/overlays/README | grep "Info")

## Firstly using $INFO, extract the four lines below the Info line from /boot/overlays/README.
## Next, extract the "Info" and "Load" lines AGAIN, 
## insert carriage returns to make them easier to read, 
## and clean up unnecessary characters, symbols, and spaces.

sudo grep -A4 "$INFO" /${bootDIR}/overlays/README \
| grep -e "Info" -e "Load" \
| sed "/Load/a \ " \
| sed -e "s/Configures //g" -e "s/the //g" -e "s/:   /:/g" -e "/Load/s/,<param>//g" -e "/Load/s/=<val>//g" -e "/Info/s/\.$//g" \
| sudo tee ./dac_list.txt.source 1>/dev/null 2>/dev/null
