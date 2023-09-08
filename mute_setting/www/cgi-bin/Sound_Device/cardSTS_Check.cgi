#!/bin/bash

# cardSTS_Check.cgi                                 #
# (C)2023 kitamura_design <kitamura_design@me.com> #

#Counting Sound Card(s)
CARDS=$(grep -c " [0-9]" /proc/asound/cards)

if [ $CARDS = 0 ]; then
        cat <<HTML
          <div class="setting-items-wrap">
          <form>
                 <input id="soundCheck" type="button" value="Sound Check" class="button-disabled" disable readonly>
                 <input class="inputbox-single-readonly" value="-- No Sound Device --" readonly>
          </form>
          </div>
HTML
else
	for ((i=0; i<$CARDS; i++)); do

          cardNAME=$(grep name /proc/asound/card$i/pcm0p/sub0/info | sed -n 1P | sed -e 's/name: //g')
      	  cardSTS=$(sed -n 1p /proc/asound/card$i/pcm0p/sub0/status | cut -d " " -f 2)
          cardNUM=$(sed -n /^card/p /proc/asound/card$i/pcm0p/sub0/info | cut -d " " -f 2)
          devNUM=$(sed -n /^device/p /proc/asound/card$i/pcm0p/sub0/info | cut -d " " -f 2)
          DEVICE="hw:${cardNUM},${devNUM}"

	  if [ ${cardSTS} = "RUNNING" ]; then
		  cardSTS=Running
	  elif [ ${cardSTS} = "closed" ]; then
		  cardSTS=Closed
          elif [ ${cardSTS} = "DRAINING" ]; then
                  cardSTS=Draining
	  fi

          cat <<HTML
           <div id="deviceSTS-$i" class="setting-items-wrap">
           <form method=GET action="/cgi-bin/Sound_Device/sound_checking.cgi" target="_self">
                 <input id="soundDevice-$i" name="sounddevice" type="hidden" value="${DEVICE}">
                 <input id="soundCheck-$i" type="submit" value="Sound Check" class="button">
		 <input class="inputbox-single-readonly" value="${cardNAME:- -- No Sound Device --}" readonly>
		 <label> ${DEVICE}</label>
                 <label><div class="status"> ${cardSTS}</div></label>
	   </form>
           </div>
HTML
        done

fi

exit 0