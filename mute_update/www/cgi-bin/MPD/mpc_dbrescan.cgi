#!/bin/bash

# mpc_dbrescan.cgi                                  #
# (C)2022 kitamura_design <kitamura_design@me.com>  #

mpc rescan --wait 2>/dev/null 1>/dev/null 

echo "Location: /cgi-bin/MPD/MPD.cgi"
echo
