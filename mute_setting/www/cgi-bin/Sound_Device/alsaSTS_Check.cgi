#!/bin/bash

# alsaSTS_Check.cgi                                 #
# (C)2023 kitamura_design <kitamura_design@me.com> #


alsaSTS=$(systemctl status alsa-state.service | grep Active: | cut -d ":" -f 2 | cut -d " " -f 3)

  if [ ${alsaSTS} = "(running)" ]; then
         echo -n "Running"
         else
         echo -n "Closed"
  fi

exit 0