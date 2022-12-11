#!/bin/bash
#Hint >> https://genzouw.com/entry/2019/02/18/122158/889/

	temp="$(cat /sys/class/thermal/thermal_zone0/temp)"

echo	$(bc <<< "scale=1; $temp/1000") "'c"
