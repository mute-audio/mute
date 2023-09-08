#!/bin/bash

# Update.cgi           			                   #
# (C)2023 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
<head>
  <link rel="stylesheet" type="text/css" href="/css/main.css?$query">

  <script type="text/javascript">
    function dispUpdate(){
        if(window.confirm('To take effect, Reboot after Updating.')){
            location.href = "/cgi-bin/Update/Updating.cgi";
        }
    }

    function dispUpdateMute(){
        if(window.confirm('Are you sure to update mute?')){
            location.href = "/cgi-bin/Update/Updating_mute.cgi";
        }
    }

    function keepHover(){
        target = parent.document.getElementById("Update");
        if (target != null){
            target.className = "menutab-keephover";
        }
    }

    function offHover(){
        target = parent.document.getElementById("Update");
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

cat <<HTML
<body id="iframe" onload="keepHover()" onunload="offHover()">

    <!-- Title -->
    <h1>Update</h1>
HTML

######## [ mute ] Update

stsUPDmute=$(cat /var/www/cgi-bin/Update/Update_mute_notice.txt)
lastUPDmute=$(sudo sed -n '$p' /var/www/cgi-bin/log/update_mute.log)

    if [ "$stsUPDmute" = "[ mute ] is up to date" ]; then

        cat <<HTML
        <!-- [ mute ] -->
        <div class="title-btn-title">
          <a href="/cgi-bin/Update/Update_checking.cgi" class="toggle-on-sw"> Check Update </a>
          <h3>[ mute ]</h3>
        </div>

        <h4>
          Last Updated : ${lastUPDmute:- Not updated yet}</br>
          ${stsUPDmute}.
        </h4>

        <div hidden id="stsUPDmute">${stsUPDmute}</div>

        <div class="separator"><hr></div>
HTML
    else

        cat <<HTML
        <!-- [ mute ] -->
        <div class="title-btn-title">
          <a href="#" onClick="dispUpdateMute(); return false;" target="_self" class="toggle-on-sw"> Update </a>
          <!-- a href="/cgi-bin/Update/Updating_mute.cgi" target="_self" class="toggle-on-sw"> Update </a -->
          <h3>[ mute ]</h3>
        <div class="status">Update Available</div>
        </div>

        <h4>
          Last Updated : ${lastUPDmute:- Not updated yet}</br>
          ${stsUPDmute}.
        </h4>

        <div hidden id="stsUPDmute">${stsUPDmute}</div>

        <div class="separator"><hr></div>
HTML
    fi

    ## MPD install check
    ## If the mpd installation is [installed,local],
    ## reinstall mpd so that automatic updates are enabled.

        mpd_Install_CHK=$(sudo apt -a -qq list mpd 2>/dev/null | grep --only-matching "installed,local")

        if [ -n "$mpd_Install_CHK" ]; then
            sudo apt install --reinstall -y mpd 2>/dev/null
        fi
    ##

######## RaspberryPi OS Update

stsUPD=$(cat /var/www/cgi-bin/Update/Update_notice.txt)
lastUPD=$(sudo sed -n '$p' /var/www/cgi-bin/log/update.log)
kernelR=$(uname -r)
kernelNAME=$(uname -s)

    if [ "$stsUPD" = "All packages are up to date." ] || [ -z "$stsUPD" ]; then

        cat <<HTML
        <!-- RaspberryPi OS -->
        <div class="title-btn-title">
          <a href="/cgi-bin/Update/Update_checking.cgi" target="mainview" class="toggle-on-sw"> Check Update </a>
          <h3>RaspberryPi OS</h3>
        </div>
HTML
    else

        cat <<HTML
        <!-- RaspberryPi OS Update Available-->
        <div class="title-btn-title">
          <a href="#" onClick="dispUpdate(); return false;" target="_self" class="toggle-on-sw"> Update </a>
          <h3>RaspberryPi OS</h3>
          <div class="status">Update Available</div>
        </div>
HTML
    fi
        cat <<HTML
        <h4>
          Kernel Ver. : ${kernelNAME} ${kernelR}</br>
          Last Updated : ${lastUPD:- Not updated yet}</br>
          ${stsUPD}
        </h4>

        <div hidden id="stsUPD">${stsUPD}</div>

    <div class="separator"><hr></div>

    <script>

    function watchUpdateOS() {
     fetch("/cgi-bin/Update/Update_notice.txt")
      .then((response) => response.text())
      .then((text) => {
        if ( text !== "All packages are up to date.\n" ) {
            fetch("/cgi-bin/Update/Update.cgi")
              .then((response) => response.text())
              .then((text) => {
                const textToHTML = document.createElement('div');
                textToHTML.innerHTML = text

                const rpiOverWrite = textToHTML.querySelector('#RPi_OS');
                const RPiOSDiv = document.querySelector('#RPi_OS');

                RPiOSDiv.innerHTML = rpiOverWrite.innerHTML;
//                console.log('RPi-OS : Updates are available.');
                return true;
               })
         }else{
//            console.log('RPi-OS : No Update');
            return false;
        }
      })
      .catch((error) => console.log(error))

      setTimeout ("watchUpdateOS()" , 60000)
    }
    
    watchUpdateOS();

    function watchUpdateMute() {
     fetch("/cgi-bin/Update/Update_mute_notice.txt")
      .then((response) => response.text())
      .then((text) => {
        if ( text !== "[ mute ] is up to date\n" ) {
            fetch("/cgi-bin/Update/Update.cgi")
              .then((response) => response.text())
              .then((text) => {

                const textToHTML = document.createElement('div');
                textToHTML.innerHTML = text;

                const muteOverWrite = textToHTML.querySelector('#mute');
                const muteDiv = document.querySelector('#mute');

                muteDiv.innerHTML = muteOverWrite.innerHTML;
//                console.log('mute : Updates are available.');
                return true;
              })
         }else{
//            console.log('mute : No Update.');
            return false;
         }
      })
      .catch((error) => console.log(error))

      setTimeout ("watchUpdateMute()" , 60000)
    }

    watchUpdateMute();
    
    </script>

  </body>
</html>
HTML
