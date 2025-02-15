#!/bin/bash

# Update.cgi           			                   #
# (C)2023 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
<head>
  <link rel="stylesheet" type="text/css" href="/css/main.css">

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

    function dispUpdateMPD(){
        if(window.confirm('Are you sure to update MPD?')){
            location.href = "/cgi-bin/Update/Updating_MPD.cgi";
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

current_VER_mute=$(grep ver /var/www/cgi-bin/etc/mute.conf | cut -d "=" -f 2)
stsUPDmute=$(cat /var/www/cgi-bin/Update/Update_mute_notice.txt)
lastUPDmute=$(sudo sed -n '$p' /var/www/cgi-bin/log/update_mute.log)

    if [ "$stsUPDmute" = "[ mute ] is up to date" ]; then

        cat <<HTML
        <!-- [ mute ] -->
      <div id="mute">
        <div class="title-btn-title">
          <a href="/cgi-bin/Update/Update_checking.cgi" class="toggle-on-sw"> Check Update </a>
          <h3>[ mute ]</h3>
        </div>

        <h4>
          Ver.${current_VER_mute}<br>
          Last Updated : ${lastUPDmute:- Not updated yet}<br>
          ${stsUPDmute}.
        </h4>

        <div hidden id="stsUPDmute">${stsUPDmute}</div>
      </div>

        <div class="separator"><hr></div>
HTML
    else

        cat <<HTML
        <!-- [ mute ] -->
      <div id="mute">
        <div class="title-btn-title">
          <a href="#" onClick="dispUpdateMute(); return false;" target="_self" class="toggle-on-sw"> Update </a>
          <!-- a href="/cgi-bin/Update/Updating_mute.cgi" target="_self" class="toggle-on-sw"> Update </a -->
          <h3>[ mute ]</h3>
        <div class="status">Update Available</div>
        </div>

        <h4>
          Ver.${current_VER_mute}<br>
          Last Updated : ${lastUPDmute:- Not updated yet}<br>
          ${stsUPDmute}
        </h4>

        <div hidden id="stsUPDmute">${stsUPDmute}</div>
      </div>

        <div class="separator"><hr></div>
HTML
    fi

####### MPD update check
      # Show MPD update button if a package newer than "mpd/now" exists

     mpd_List=$(cat /var/www/cgi-bin/Update/Update_MPD_notice.txt)
     mpd_Install_CHK=$(echo $mpd_List | wc -l)
     newPKG=$(echo $mpd_List | sed -n 1p)

     if [ $mpd_Install_CHK = 2 ]; then

        cat <<HTML
        <!-- MPD -->
        <div id="MPD">
          <div class="title-btn-title">
            <a href="#" onClick="dispUpdateMPD(); return false;" target="_self" class="toggle-on-sw"> Update </a>
            <h3>MPD</h3>
          <div class="status">Update Available</div>
          </div>

          <h4>
            New Package Found : ${newPKG}<br>
          </h4>
        </div>

        <div class="separator"><hr></div>
HTML

     else

        cat <<HTML
        <!-- MPD -->
        <div id="MPD">
        </div>

HTML

     fi

######## RaspberryPi OS Update

stsUPD=$(cat /var/www/cgi-bin/Update/Update_notice.txt)
lastUPD=$(sudo sed -n '$p' /var/www/cgi-bin/log/update.log)
kernelR=$(uname -r)
kernelNAME=$(uname -s)

    if [ "$stsUPD" = "All packages are up to date." ] || [ -z "$stsUPD" ]; then

        cat <<HTML
        <!-- RaspberryPi OS -->
      <div id="RPi_OS">
        <div class="title-btn-title">
          <a href="/cgi-bin/Update/Update_checking.cgi" target="mainview" class="toggle-on-sw"> Check Update </a>
          <h3>RaspberryPi OS</h3>
        </div>
HTML
    else

        cat <<HTML
        <!-- RaspberryPi OS Update Available-->
      <div id="RPi_OS">
        <div class="title-btn-title">
          <a href="#" onClick="dispUpdate(); return false;" target="_self" class="toggle-on-sw"> Update </a>
          <h3>RaspberryPi OS</h3>
          <div class="status">Update Available</div>
        </div>
HTML
    fi
        cat <<HTML
        <h4>
          Kernel Ver. : ${kernelNAME} ${kernelR}<br>
          Last Updated : ${lastUPD:- Not updated yet}<br>
          ${stsUPD}
        </h4>

        <div hidden id="stsUPD">${stsUPD}</div>
    </div>

    <div class="separator"><hr></div>

    <script>

    function watchUpdate() {
     const beforeOSdiv = document.querySelector('#RPi_OS');
     const beforeMutediv = document.querySelector('#mute');

     fetch("/cgi-bin/Update/Update.cgi")
      .then((response) => response.text())
      .then((text) => {
         const textToHTML = document.createElement('div');
         textToHTML.innerHTML = text

         const afterOSdiv = textToHTML.querySelector('#RPi_OS');
         const afterMutediv = textToHTML.querySelector('#mute');

         beforeOSdiv.innerHTML = afterOSdiv.innerHTML;
         beforeMutediv.innerHTML = afterMutediv.innerHTML;

      })
      .catch((error) => console.log(error))

      setTimeout (watchUpdate , 60000)
    }

    watchUpdate();

    </script>

  </body>
</html>
HTML
