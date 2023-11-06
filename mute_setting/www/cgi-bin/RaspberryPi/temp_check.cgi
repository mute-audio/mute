#!/bin/bash

# temp_check.cgi.cgi                               #
# (C)2023 kitamura_design <kitamura_design@me.com> #

temp=$(cat /sys/class/thermal/thermal_zone0/temp)
TEMP=$(bc <<< "scale=1; $temp/1000") 

cat <<HTML
<div id="temp">CPU Temp : ${TEMP} c˚</div>
HTML