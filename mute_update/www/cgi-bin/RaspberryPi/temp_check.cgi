#! /bin/bash

temp="$(cat /sys/class/thermal/thermal_zone0/temp)"
TEMP="$(bc <<< "scale=1; $temp/1000") c˚"

echo "CPU Temp : ${TEMP}"
