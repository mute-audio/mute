#!/bin/bash

# stop_sp_test.cgi                                 #
# (C)2022 kitamura_design <kitamura_design@me.com> #

# Kill speaker-test by PID 
 PID_sptest=$(pgrep -lf speaker-test | grep speaker-test | cut -d " " -f 1)
 sudo kill -2 ${PID_sptest}

# Go back to the Page
 echo "Location: /cgi-bin/Sound_Device/Sound_device.cgi"
 echo ''
