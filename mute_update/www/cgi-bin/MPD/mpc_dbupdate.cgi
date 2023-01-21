#!/bin/bash

# mpc_dbupdate.cgi		                           #
# (C)2022 kitamura_design <kitamura_design@me.com> #

mpc update --wait 2>/dev/null 1>/dev/null

echo "Location: /cgi-bin/MPD/check_MPD.cgi"
echo ''
