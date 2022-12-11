#!/bin/bash

# mpc_dbupdate.cgi		                           #
# (C)2022 kitamura_design <kitamura_design@me.com> #

mpc update --wait

echo "Location: /cgi-bin/MPD/check_MPD.cgi"
echo ''
