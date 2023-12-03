#!/bin/bash

# alsaSTS_Check.cgi                                 #
# (C)2023 kitamura_design <kitamura_design@me.com> #


alsaSTS=$(systemctl status alsa-state.service | grep Active: | cut -d ":" -f 2 | cut -d " " -f 3)

  if [ ${alsaSTS} = "(running)" ]; then
    alsaSTATUS="Running"
  else
    alsaSTATUS="Closed"
  fi

cat <<HTML
<div id="alsa-STS" class="status">${alsaSTATUS}</div>
HTML

exit 0