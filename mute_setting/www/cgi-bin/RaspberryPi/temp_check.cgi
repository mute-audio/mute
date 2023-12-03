#!/bin/bash

# temp_check.cgi.cgi                               #
# (C)2023 kitamura_design <kitamura_design@me.com> #

TEMP=$(sudo vcgencmd measure_temp | cut -d "=" -f 2)

cat <<HTML
<div id="temp">CPU Temp : ${TEMP} </div>
HTML