#!/bin/bash

# MPD.cgi                                          #
# (C)2022 kitamura_design <kitamura_design@me.com> #

#### General options Status @/etc/mpd.conf
 bindADD=$(sudo grep bind_to_address /etc/mpd.conf | sed -n 1p | cut -d "\"" -f 2 | cut -d "\"" -f 1)
 autoUPDATE=$(sudo grep auto_update /etc/mpd.conf | sed -n 1p | cut -d "\"" -f 2 | cut -d "\"" -f 1)
 rstPAUSE=$(sudo grep restore_paused /etc/mpd.conf | cut -d "\"" -f 2 | cut -d "\"" -f 1)
 audioBUFFER=$(sudo grep audio_buffer_size /etc/mpd.conf | cut -d "\"" -f 2 | cut -d "\"" -f 1)
 sampleRATE=$(sudo grep samplerate_converter /etc/mpd.conf | cut -d "\"" -f 2 | cut -d "\"" -f 1)
 UTF8=$(sudo grep filesystem_charset /etc/mpd.conf | grep "#" | cut -f 1)
 mpdLOG=$(sudo grep log_file /etc/mpd.conf | grep "#" | cut -f 1)

#### Audio output Status @/etc/mpd.conf
 nameSTUS=$(sed -n /^#ALSA$/,/\}/p /etc/mpd.conf | grep '^.name.*' | cut -d "\"" -f 2)
 hWSTUS=$(sed -n /^#ALSA$/,/}/p /etc/mpd.conf | grep '^.device.*' | cut -d "\"" -f 2 | sed -n 1p)
 dopSTUS=$(sed -n /^#ALSA$/,/}/p /etc/mpd.conf | grep '^.dop.*' | cut -d "\"" -f 2)
 resmpleSTUS=$(sed -n /^#ALSA$/,/}/p /etc/mpd.conf | grep '^.auto_resample.*' | cut -d "\"" -f 2)
 mixerTYPE=$(sed -n /^#ALSA$/,/}/p /etc/mpd.conf | grep '^.mixer_type.*' | cut -d "\"" -f 2)
 mixerCTL=$(sed -n /^#ALSA$/,/}/p /etc/mpd.conf | grep '^.mixer_control.*' | cut -d "\"" -f 2)

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>

  <head>
    <link rel="stylesheet" type="text/css" href="/css/main.css?$query">
    <script>

      function keepHover(){
                target = parent.document.getElementById("MPD");
                if (target != null){
                        target.className = "menutab-keephover";
                }
        }

      function offHover(){
                target = parent.document.getElementById("MPD");
                if (target != null){
                        target.className = "menutab";
                }
        }

      function toggleOff(){
                let base_id = event.srcElement.id;
                let base = document.getElementById(base_id);
                let tglwrap = base.nextElementSibling;
                target = tglwrap.firstElementChild;
                if (target != null){
                        target.className = "toggle-on-mark-off";
                }
        }

      function toggleOn(){
                let base_id = event.srcElement.id;
                let base = document.getElementById(base_id);
                let tglwrap = base.previousElementSibling;
                target = tglwrap.firstElementChild;
                if (target != null){
                        target.className = "toggle-off-mark-on";
                }
        }

    </script>
  </head>
HTML

 ## MPD install check
 ## If the mpd installation is [installed,local],
 ## reinstall mpd so that automatic updates are enabled.
   mpd_Install_CHK=$(sudo apt -a -qq list mpd 2>/dev/null | grep --only-matching "installed,local")
   if [ -n "$mpd_Install_CHK" ]; then
      sudo apt install --reinstall -y mpd 2>/dev/null
   fi

#### MPD_V.txt check
if [ ! -e /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt ]; then
   mpd -V | sudo tee /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt > /dev/null
fi

  cat <<HTML
  <body id="iframe" onLoad="keepHover()" onunload="offHover()">
HTML

#### MPD check
MPDSTATUS=$(systemctl status mpd | grep Active: | sed 's/^[ \t]*//' | cut -d"(" -f2 | cut -d")" -f1)
mpdVER=$(grep "Music Player Daemon" /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt | cut -d " " -f 4)
mpdPKG=$(grep pkg /var/www/cgi-bin/etc/mute.conf | cut -d "=" -f 2)

if [ "$MPDSTATUS" = "running" ]; then
        StatusMPD=Running
else
        StatusMPD=Stopped
fi

    cat <<HTML
    <!-- Title -->
    <h1>MPD</h1>

      <!-- MPD Restart -->
      <div class="title-btn-title">
         <a href="/cgi-bin/MPD/MPDrestarting.cgi" target="mainview" class="toggle-on-sw"> Restart MPD </a>
         <h3>Music Player Deamon <div class="status">${StatusMPD}</div> </h3>
      </div>

      <!-- MPD Status -->
      <h4>$(mpc stats | sed -n 5,6p | sed -e 'a\<br>')
        Package : ${mpdPKG}<br>
        Version : ${mpdVER}</h4>

      <div class="separator"><hr></div>

      <!-- Music Database -->
      <div class="title-btn-title">
         <a href="/cgi-bin/MPD/DBupdating.cgi" target="mainview" class="button"> Update DB </a>
         <a href="/cgi-bin/MPD/DBrescanning.cgi" target="mainview" class="button2"> Rescan DB </a>
         <h3>Music Database</h3>
      </div>

      <!-- Database Status -->
      <h4>$(mpc stats | sed -n 1,3p | sed -e 'a\<br>')
      $(mpc stats | grep 'DB Updated')</h4>

      <div class="separator"><hr></div>
HTML

#### mpd.conf

      cat <<HTML
      <!-- MPD conf. Title & Reset Btn -->
      <div class="title-btn-title">
         <a href="/cgi-bin/MPD/MPD_conf_resetting.cgi" target="mainview" class="toggle-on-sw"> Reset </a>
         <h3 id="mpdconfig">MPD Config.</h3>
      </div>

      <!-- General Options -->
      <div><h4 id="generaloption">General Options</h4></div>

      <div>
        <!-- bind to address :text-input -->
        <form method=GET action="/cgi-bin/MPD/MPD_conf/bind_to_address_processing.cgi" target="_self">
          <div class="setting-items-wrap">
          <input id="Apply" type="submit" value="Set" class="button"></input>
          <div class="ellipsis-wrap">Aa</div>
          <input type="text" id="bindADD" name="bindADD" value="${bindADD}" class="inputbox-single" required>
          <label for="">Bind to Address</label>
          </div>
        </form>

        <!-- audio buffer size :input -->
        <form method=GET action="/cgi-bin/MPD/MPD_conf/audio_buffer_size_processing.cgi" target="_self">
          <div class="setting-items-wrap">
          <input id="Apply" type="submit" value="Set " class="button"></input>
          <div class="ellipsis-wrap">123</div>
          <input type="tel" id="bufferSIZE" name="bufferSIZE" value="${audioBUFFER}" class="inputbox-single" required>
          <label for="">Audio Buffer Size</label>
          </div>
        </form>
HTML

#### auto update Toggle SW

        if [ "$autoUPDATE" = "yes" ]; then

          cat <<HTML
          <!-- auto_update :Toggle SW Yes-->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="auto_update_btn" href="/cgi-bin/MPD/MPD_conf/auto_update_processing.cgi?autoUPDATE=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>Auto Update</label>
          </div>
HTML
        else
          cat <<HTML
          <!-- auto_update :Toggle SW No-->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="auto_update_btn" href="/cgi-bin/MPD/MPD_conf/auto_update_processing.cgi?autoUPDATE=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>Auto Update</label>
          </div>
HTML
        fi

### restore paused :Toggle SW

        if [ "$rstPAUSE" = "yes" ]; then

          cat <<HTML
          <!-- restore paused :Toggle SW Yes -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="restore_paused_btn" href="/cgi-bin/MPD/MPD_conf/restore_paused_processing.cgi?rstPAUSED=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>Restore Paused</label>
          </div>
HTML
        else
          cat <<HTML
          <!-- restore paused :Toggle SW No -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="restore_paused_btn" href="/cgi-bin/MPD/MPD_conf/restore_paused_processing.cgi?rstPAUSED=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>Restore Paused</label>
          </div>
HTML
        fi

#### filesystem_charset :UTF-8

        if [ "$UTF8" = "#filesystem_charset" ]; then

          cat <<HTML
          <!-- UTF-8 :Toggle SW No -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="utf8_btn" href="/cgi-bin/MPD/MPD_conf/UTF8_processing.cgi?UTF8=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>UTF-8 Charset</label>
          </div>
HTML
        else

          cat <<HTML
          <!-- UTF-8 :Toggle SW Yes -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="utf8_btn" href="/cgi-bin/MPD/MPD_conf/UTF8_processing.cgi?UTF8=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
              <div class="toggle-on-wrap"><div id="tgl-on" class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>UTF-8 Charset</label>
          </div>
HTML
        fi

#### log On/ Off

        if [ "$mpdLOG" = "#log_file" ]; then

          cat <<HTML
          <!-- Log :Toggle SW No -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="log_file_btn" href="/cgi-bin/MPD/MPD_conf/mpd_log_processing.cgi?mpd_log=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>Log file</label>
          </div>
HTML
        else

          cat <<HTML
          <!-- Log :Toggle SW Yes -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="log_file_btn" href="/cgi-bin/MPD/MPD_conf/mpd_log_processing.cgi?mpd_log=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>Log file</label>
          </div>
HTML
        fi

##### Input Options

CURL=$(sed -n /input\ \{/,/\}/p /etc/mpd.conf | grep -B 1 'plugin.*\"curl\"' | sed -n /.*enabled.*/p | cut -d "\"" -f 2 | cut -d "\"" -f 1)
QOBUZ=$(sed -n /input\ \{/,/\}/p /etc/mpd.conf | grep -B 1 'plugin.*\"qobuz\"' | sed -n /.*enabled.*/p | cut -d "\"" -f 2 | cut -d "\"" -f 1)

        cat <<HTML
      <!-- Input Plugins -->
      <h4 id="inputplugin">Input Plugins</h4>
HTML

#### CURL check

        if [ "$CURL" = "no" ]; then

          cat <<HTML
          <!-- CURL Toggle No-->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="curl_btn" href="/cgi-bin/MPD/MPD_conf/curl_processing.cgi?CURL=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>CURL</label>
          </div>
HTML
        elif [ "$CURL" = "yes" ]; then

          cat <<HTML
          <!-- CURL Toggle Yes-->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="curl_btn" href="/cgi-bin/MPD/MPD_conf/curl_processing.cgi?CURL=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>CURL</label>
          </div>
HTML
        elif [ -z "$CURL" ]; then

          cat <<HTML
          <!-- CURL Toggle N/A-->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a class="toggle-off-sw">Not assigned</a>
            </div>
            <input class="inputbox-single-invisible" value="NA" readonly></input>
            <label>CURL</label>
          </div>
HTML
        fi

#### QOBUZ check

#        if [ "$QOBUZ" = "no" ]; then

#         cat <<HTML
#          <!-- QOBUZ Toggle No -->
#          <div class="setting-items-wrap">
#            <div class="toggle-wrap">
#              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
#              <a id="qobuz_btn" href="/cgi-bin/MPD/MPD_conf/qobuz_processing.cgi?QOBUZ=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
#            </div>
#            <input class="inputbox-single-invisible" value="No" readonly></input>
#            <label>QOBUZ</label>
#          </div>
#HTML
#        elif [ "$QOBUZ" = "yes" ]; then

#          cat <<HTML
#          <!-- QOBUZ Toggle Yes -->
#          <div class="setting-items-wrap">
#            <div class="toggle-wrap">
#              <a id="qobuz_btn" href="/cgi-bin/MPD/MPD_conf/qobuz_processing.cgi?QOBUZ=No" onClick="toggleOff" target="_self" class="toggle-on-sw">Yes</a>
#              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
#            </div>
#            <input class="inputbox-single-invisible" value="Yes" readonly></input>
#            <label>QUBUZ</label>
#          </div>
#HTML
#        elif [ -z "$QOBUZ" ]; then

#          cat <<HTML
#          <!-- QOBUZ Toggle N/A -->
#          <div class="setting-items-wrap">
#            <div class="toggle-wrap">
#              <a href="" target="_self" class="toggle-off-sw">Not assigned</a>
#            </div>
#            <input class="inputbox-single-invisible" value="NA" readonly></input>
#            <label>QOBUZ</label>
#          </div>
#HTML
#        fi

#          cat <<HTML
#          <div class=\separator"></div>
#HTML

          cat <<HTML
          <!-- QOBUZ N/A-->
          <div class="setting-items-wrap">
            <a class="toggle-off-sw">Not Available</a>
            <input class="inputbox-single-invisible" value="NA" readonly></input>
            <label>QOBUZ</label>
          </div>
HTML

###### Audio_Output

          cat <<HTML
          <!-- Input Plugins -->
          <h4 id="output">Audio Output</h4>
HTML

##### Output Select
CARDS=$(grep -c " [0-9]" /proc/asound/cards)

          cat <<HTML
          <!-- Output Select -->
          <form method=GET action="/cgi-bin/MPD/MPD_conf/audio_output_processing_name.cgi" target="_self">
            <div class="setting-items-wrap">
              <input id="Apply" type="submit" value="Select " class="button"></input>
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select  id="output_select" name="name" class="inputbox-single">
                <option>${nameSTUS} (${hWSTUS})</option>
HTML
                for ((i=0; i<$CARDS; i++)); do

                  cardNAME=$(grep name /proc/asound/card$i/pcm0p/sub0/info | sed -n 1P | sed -e 's/name: //g')
                  cardNUM=$(sed -n /^card/p /proc/asound/card$i/pcm0p/sub0/info | cut -d " " -f 2)
                  devNUM=$(sed -n /^device/p /proc/asound/card$i/pcm0p/sub0/info | cut -d " " -f 2)
                  DEVICE="hw:${cardNUM},${devNUM}"

                  cat <<HTML
                  <option>${cardNAME} (${DEVICE})</option>
HTML
                done

              cat <<HTML
              </select>
              <label for="">Output Select</label>
            </div>
          </form>
HTML

#### mixer type

if [ "$mixerTYPE" = "software" ]; then
        mixerTYPE_A=Software
        mixerTYPE_B=Hardware
        mixerTYPE_C=Disabled

elif [ "$mixerTYPE" = "hardware" ]; then
        mixerTYPE_A=Hardware
        mixerTYPE_B=Disabled
        mixerTYPE_C=Software

elif [ "$mixerTYPE" = "disabled" ]; then
        mixerTYPE_A=Disabled
        mixerTYPE_B=Software
        mixerTYPE_C=Hardware
fi
          cat <<HTML
          <!-- Mixer Type -->
          <form method=GET action="/cgi-bin/MPD/MPD_conf/audio_output_processing.cgi" target="_self">
            <div class="setting-items-wrap">
              <input id="Apply" type="submit" value="Apply" class="button"></input>
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select  id="mixertype" name="mixertype" class="inputbox-single">
                 <option selected>${mixerTYPE_A}</option>
                 <option >${mixerTYPE_B}</option>
                 <option >${mixerTYPE_C}</option>
              </select>
              <label for="">Mixer Type</label>
            </div>
          </form>
HTML

#### mixer Control in case mixer_type set hardware
if [ "$mixerTYPE" = "hardware" ]; then

CTL_option=$(amixer scontrols | cut -d "'" -f 2 | sed -e "s/^/<option>/g" -e "s/$/<\/option>/g")

          cat <<HTML
          <!-- Mixer Control -->
          <form method=GET action="/cgi-bin/MPD/MPD_conf/audio_output_processing.cgi" target="_self">
            <div class="setting-items-wrap">
              <input id="Apply" type="submit" value="Apply" class="button"></input>
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select  id="mixerctle" name="mixerctl" class="inputbox-single">
                <option selected>${mixerCTL}</option>
                $CTL_option
              </select>
              <label for="">Mixer Control</label>
            </div>
          </form>
HTML
fi

#### DOP On/ Off

        if [ "$dopSTUS" = "no" ]; then

          cat <<HTML
          <!-- DOP No -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="dop_btn" href="/cgi-bin/MPD/MPD_conf/audio_output_processing.cgi?dop=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>DSD on PCM ( DoP )</label>
            </div>
HTML
        else

          cat <<HTML
          <!-- DOP Yes -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="dop_btn" href="/cgi-bin/MPD/MPD_conf/audio_output_processing.cgi?dop=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>DSD on PCM ( DoP )</label>
          </div>
HTML
        fi

#### Auto Resample On/ Off

        if [ "$resmpleSTUS" = "no" ]; then

          cat <<HTML
          <!-- Auto Resample No -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="resamle_btn" href="/cgi-bin/MPD/MPD_conf/audio_output_processing.cgi?resample=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>Auto Resample</label>
          </div>
HTML
        else

          cat <<HTML
          <!-- Auto Resample Yes -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="resample_btn" href="/cgi-bin/MPD/MPD_conf/audio_output_processing.cgi?resample=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>Auto Resample</label>
          </div>
HTML
        fi

#### HTTP Streaming
          cat <<HTML
          <h4 id="httpd">HTTP Streaming</h4>
HTML

#### HTTPD status check
HTTPD=$(sed -n /audio_output\ \{/,/\}/p /etc/mpd.conf | grep -B 1 '\"httpd\"' | sed -n /audio_output/p | cut -d " " -f 1)

        if [ "$HTTPD" = "#audio_output" ]; then

          cat <<HTML
          <!-- HTTP Server Disabled -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
              <a id="httpd_btn" href="/cgi-bin/MPD/MPD_conf/httpd_sw_processing.cgi?HTTPD=On" onClick="toggleOn()" target="_self" class="toggle-off-sw">Disabled</a>
            </div>
            <input class="inputbox-single-invisible" value="No" readonly></input>
            <label>HTTP Server</label>
          </div>
HTML
        elif [ "$HTTPD" = "audio_output" ]; then

        #### Check HTTPD Setting Status
	  httpdserverNAME=$(sed -n /^#HTTPD$/,/\}/p /etc/mpd.conf | grep '^.name.*' | cut -d "\"" -f 2)
	  httpdportNUM=$(sed -n /^#HTTPD$/,/\}/p /etc/mpd.conf | grep '^.port.*' | cut -d "\"" -f 2)
	  encoderSTUS_A=$(sed -n /^#HTTPD$/,/\}/p /etc/mpd.conf | grep '^.encoder.*' | cut -d "\"" -f 2)
	  httpdBPS=$(sed -n /^#HTTPD$/,/\}/p /etc/mpd.conf | grep '^.bitrate.*' | cut -d "\"" -f 2)

        #### Set Decoder
	  if [ "$encoderSTUS_A" = vorbis ]; then
	    encoderSTUS_B=lame
	  else
	    encoderSTUS_B=vorbis
	  fi

          cat <<HTML
          <!-- HTTP Server Enabled -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a id="httpd_btn" href="/cgi-bin/MPD/MPD_conf/httpd_sw_processing.cgi?HTTPD=Off" onClick="toggleOff()" target="_self" class="toggle-on-sw">Enabled</a>
              <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
            </div>
            <input class="inputbox-single-invisible" value="Yes" readonly></input>
            <label>HTTP Server</label>
          </div>

          <!-- HTTP Server Setting form -->          
          <div>
          <form method=GET action="/cgi-bin/MPD/MPD_conf/httpd_conf_processing.cgi" target="_self">

            <!-- Server Name -->
            <div class="setting-items-wrap">
              <div class="ellipsis-wrap">Aa</div>
              <input type="text" id="http_server" name="http_server" value="${httpdserverNAME}" class="inputbox" required>
              <label for="">Sever Name</label>
            </div>

            <!-- Port number -->
            <div class="setting-items-wrap">
              <div class="ellipsis-wrap">123</div>
              <input type="text" id="httpd_port" name="httpd_port" value="${httpdportNUM}" class="inputbox" required>
              <label for="">Port</label>
            </div>

            <!-- Encoder List-->
            <li class="setting-items-wrap">
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select  id="encoder" name="encoder" class="inputbox">
                <option selected>${encoderSTUS_A}</option>
                <option >${encoderSTUS_B}</option>
              </select>
              <label for="">Encoder</label>
            </li>

            <!-- Bitrate -->
            <div class="setting-items-wrap">
              <div class="ellipsis-wrap">123</div>
              <input type="text" id="httpd_rate" name="httpd_rate" value="${httpdBPS}" class="inputbox" required>
              <label for="">Bitrate ( bps )</label>
            </div>

            <!-- Reset/ Submit -->
            <input id="submit" type="submit" value="Apply " class="button"></input>
            <input id="reset" type="reset" value=" Reset " class="button2"></input>

	  </form>
	  </div>
HTML
        elif [ -z "$HTTPD" ]; then

          cat <<HTML
          <!-- HTTPD Not assigned -->
          <div class="setting-items-wrap">
            <div class="toggle-wrap">
              <a class="toggle-off-sw">Not assigned</a>
            </div>
            <input class="inputbox-single-invisible" value="NA" readonly></input>
            <label>HTTp Server</label>
          </div>
HTML
        fi


#### Decoder Plugin
          cat <<HTML
          <h4 id="decoder">Decoder Plugins</h4>
HTML

######  Plugin Selector Toggle SW
DECODER=$(sed -n /Decoders\ plugins/,/Filters/p /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt | egrep  --only-matching '\[.+\]' | cut -d "[" -f 2 | cut -d "]" -f 1)

          cat <<HTML
          <div>
HTML
	  for decoder in ${DECODER[@]}; do

		plugin=$(< /etc/mpd.conf grep -A 1 plugin.*\"${decoder}\" | sed -n /.*enabled.*/p | cut -d "\"" -f 2  | cut -d "]" -f 1)
                format=$(grep "\[${decoder}\]" /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt | cut -d "]" -f 2 | sed -e 's/^ //g')

		if [ "$plugin" = "no" ]; then

                  cat <<HTML
                  <!-- Decoder Nn -->
                  <div class="setting-items-wrap">
                    <div class="toggle-wrap">
                      <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
                      <a id="${decoder}" href="/cgi-bin/MPD/MPD_conf/decoder_processing.cgi?${decoder}=Yes" onClick="toggleOn()" target="_self" class="toggle-off-sw">No</a>
                    </div>
                    <span id="tooltips" class="description">${format}</span>
                    <label>${decoder}</label>
                  </div>
HTML
		elif [ "$plugin" = "yes" ]; then

                  cat <<HTML
                  <!-- Decoder Yes -->
                  <div class="setting-items-wrap">
                    <div class="toggle-wrap">
                      <a id="${decoder}" href="/cgi-bin/MPD/MPD_conf/decoder_processing.cgi?${decoder}=No" onClick="toggleOff()" target="_self" class="toggle-on-sw">Yes</a>
                      <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
                    </div>
                    <span id="tooltips" class="description">${format}</span>
                    <label>${decoder}</label>
                  </div>
HTML
		elif [ -z "$plugin" ]; then

                  cat <<HTML
                  <!-- Decoder Not assigned -->
                  <div class="setting-items-wrap">
                    <div class="toggle-wrap">
                      <a href="" target="_self" class="toggle-off-sw">Not assigned</a>
                    </div>
                    <span id="tooltips" class="description">${format}</span>
                    <label>${decoder}</label>
                  </div>
HTML
		fi
	  done

          cat <<HTML
          </div>

        <div class="separator"><hr><br></div>

  </body>
</html>
HTML
