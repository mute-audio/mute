#!/bin/bash

# cardSTS_Check.cgi                                 #
# (C)2026 kitamura_design <kitamura_design@me.com> #
# Collaborated with Gemini

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
		 <input class="inputbox-single-readonly" value="${DEVICE} : ${cardNAME:- -- No Sound Device --}" readonly>
                 <label><div class="status"> ${cardSTS}</div></label>
	   </form>
           </div>
HTML

          #### DSP Filters
          ## Checking DAC with DSP filters
          for card in $(aplay -l | grep '^card' | awk '{print $2}' | tr -d ':'); do
              NUMID=$(amixer -c $card contents | grep "name='DSP Program'" | sed -n 's/.*numid=\([0-9]*\).*/\1/p')
                if [ -n "$NUMID" ]; then
                    CARD_INDEX=$card
                    break
                fi
          done

          # Genarate UI only if DAC with DSP filter
          if [ -n "$CARD_INDEX" ]; then
            ITEMS_COUNT=$(amixer -c $CARD_INDEX contents | grep -A 1 "numid=$NUMID," | grep "items=" | sed 's/.*items=//' | tr -d '[:space:]')
            CURRENT_VAL=$(amixer -c $CARD_INDEX contents | sed -n "/numid=$NUMID,/,/numid=/p" | grep "^  : values=" | cut -d'=' -f2 | tr -d '[:space:]')

            # safty for null
            : ${CURRENT_VAL:=0}

            cat <<HTML
            <div id="dsp_filter" class="setting-items-wrap">
                <div class="ellipsis-wrap"><div class="allow-down"></div></div>
                <select name="dsp_filter" class="inputbox" onfocus="isOperating = true;" onblur="isOperating = false;" onchange="applyFilter($CARD_INDEX, $NUMID, this.value)">
HTML
                for i in $(seq 0 $((ITEMS_COUNT - 1))); do
                    ITEM_NAME=$(amixer -c $CARD_INDEX contents | sed -n "/numid=$NUMID,/,/numid=/p" | grep "Item #$i " | cut -d"'" -f2)

                    # Set “selected” only if the value matches the current value
                    SELECTED=""
                    if [ "$i" = "$CURRENT_VAL" ]; then
                        SELECTED="selected"
                    fi

                cat <<HTML
                <option value="$i" $SELECTED>$ITEM_NAME</option>
HTML
                done

            cat <<HTML
            </select>
            <label id="dac_list">Digital Filter</label>
            </div>
HTML
          fi
        done
fi

exit 0