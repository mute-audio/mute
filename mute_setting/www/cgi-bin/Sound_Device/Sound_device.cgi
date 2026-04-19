#!/bin/bash

# Sound_device.cgi                                 #
# (C)2026 kitamura_design <kitamura_design@me.com> #

#Generate HTML Tag source file
grep Load /var/www/cgi-bin/dac_list/dac_list.txt \
    | cut -d ":" -f 2 | cut -d "=" -f 2 \
    | sed -e 's/^/<option value=\"/g' -e 's/$/\">/g' \
    | sudo tee /var/www/cgi-bin/dac_list/dac_value.txt > /dev/null

grep Info /var/www/cgi-bin/dac_list/dac_list.txt  \
    | cut -d ":" -f 2 | sed -e 's/$/<\/option>/g' \
    | sudo tee /var/www/cgi-bin/dac_list/dac_label.txt > /dev/null

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
        <head>
          <link rel="stylesheet" type="text/css" href="/css/main.css">
          <!-- <meta http-equiv="Refresh" content="30"> -->
          <script>

       		  function autoRebootMsg(){
      				if(window.confirm('Automatically Reboot after running.\nAre you sure?')){
			      		return true;
					    } else {
					    return false;
				      }
			      }

            function keepHover(){
                target = parent.document.getElementById("SoundDevice");
                if (target != null){
                        target.className = "menutab-keephover";
                        }
                }

            function offHover(){
                target = parent.document.getElementById("SoundDevice");
                if (target != null){
                        target.className = "menutab";
                        }
                }
          </script>
        </head>
HTML

#### Current DAC_info & Sound Check

#### ALSA Info
alsaSTS=$(systemctl status alsa-state.service | grep Active: | cut -d ":" -f 2 | cut -d " " -f 3)

  if [ ${alsaSTS} = "(running)" ]; then
         alsaSTS=Running
         else
         alsaSTS=Closed
  fi

  cat <<HTML
      <body id="iframe" onLoad="keepHover()" onunload="offHover()">

          <!-- Menu Title -->
          <h1>Sound Device</h1>

          <!-- Driver -->
          <div class="title-btn-title">
          <h3>Driver : Advanced Linux Sound Architecture [ ALSA ]
          <div id="alsa-STS" class="status">${alsaSTS}</div>
          </h3>
          </div>

HTML

#### Sound Devices Setting
#Counting Sound Card(s)
CARDS=$(grep -c " [0-9]" /proc/asound/cards)

  cat <<HTML
          <!-- Driver Info-->
          <h3>Sound Devices</h3>
          <div id="Device_List">
HTML

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
            <label id="dac_list">DSP Filter</label>
            </div>
HTML
          fi
      done
    fi
        cat <<HTML
        </div>
HTML

#### Device Setting
          cat <<HTML

          <h4>Device Setting</h4>

          <form method=GET action="/cgi-bin/Sound_Device/dac_applying.cgi" onsubmit="return autoRebootMsg()" target="_self">
                 <div class="setting-items-wrap">
                 <input id="dac_list" type="submit" value=" Apply " class="button"></input>
                 <div class="ellipsis-wrap"><div class="allow-down"></div></div>
                 <select  id="dac_list" name="dac_list" class="inputbox-single">
                         <option selected disabled>Choose from the list...</option>
		         <!-- Combine HTML Tag souce files to option tag -->
                         $(paste /var/www/cgi-bin/dac_list/dac_value.txt /var/www/cgi-bin/dac_list/dac_label.txt)
                 </select>
                 <label id="dac_list">I2S DAC</label>
                </div>
          </form>

          <div class="separator"><hr></div>

        <script>

       // Apply DSP filter ----
        function applyFilter(card, numid, val) {

          fetch('/cgi-bin/Sound_Device/ALSA_control.cgi?card=' + card + '&numid=' + numid + '&val=' + val)
          .then(response => {
            if (response.ok) {
                console.log("Filter changed to value: " + val);
            }
          })
          .catch(error => console.error('Error:', error));
        }

       // ALSA Status Checker -----
        function alsaSTSCheck() {
            const alsaSTS = document.querySelector('#alsa-STS');

            fetch("/cgi-bin/Sound_Device/alsaSTS_Check.cgi")
            .then( (response) => response.text())
            .then((text) => alsaSTS.outerHTML = text)
            .catch( (error) => console.log(error))

             setTimeout( alsaSTSCheck , 10000 )
        }

        alsaSTSCheck();

       // SoundDevice (DAC) Status Checker -----
        function cardSTSCheck() {
            const deviceList = document.querySelector("#Device_List");
            const URL = '/cgi-bin/Sound_Device/cardSTS_Check.cgi';

            fetch(URL)
            .then( (response) => response.text())
            .then( (text) => deviceList.innerHTML = text )
            .catch( (error) => console.log(error))

            setTimeout( cardSTSCheck , 10000 )
        }

        cardSTSCheck();

        </script>

       </body>
</html>
HTML
