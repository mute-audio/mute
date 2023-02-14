#!/bin/bash

# Update.cgi                			           #
# (C)2022 kitamura_design <kitamura_design@me.com> #

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

    function autoRebootMsg(){
        if(window.confirm('Automatically Reboot after running.\nAre you sure?')){
            return true;
            } else {
                return false;
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
ver_UPDATE=$(\
sudo wget --no-check-certificate -q -O - "https://www.dropbox.com/s/9op8f7ras6s4a94/update.info" \
    | grep "ver=" | sed -e 's/[^0-9]//g'\
)

ver_CURRENT=$(\
grep "ver=" /var/www/cgi-bin/etc/mute.conf \
    | sed -e 's/[^0-9]//g'\
)

if [[ "$ver_UPDATE" -gt "$ver_CURRENT" ]]; then
    stsUPDmute="[ mute ] Update available"
else
    stsUPDmute="[ mute ] is up to date"
fi

lastUPDmute=$(sudo sed -n '$p' /var/www/cgi-bin/log/update_mute.log)

    if [ "$stsUPDmute" = "[ mute ] is up to date" ]; then

        cat <<HTML
        <!-- [ mute ] -->
        <div class="title-btn-title">
          <a href="" class="toggle-off-sw"> Update </a>
          <h3>[ mute ]</h3>
        </div>
        
            <h4>
            Last Updated : ${lastUPDmute:- Not updated yet}</br>
            ${stsUPDmute}.
            </h4>

    <div class="separator"><hr></div>
HTML
    else

        cat <<HTML
        <!-- [ mute ] -->
        <div class="title-btn-title">
          <a href="/cgi-bin/Update/Updating_mute.cgi" target="_self" class="toggle-on-sw"> Update </a>
          <h3>[ mute ]</h3>
        <div class="status">Update Available</div>
        </div>

            <h4>
            Last Updated : ${lastUPDmute:- Not updated yet}</br>
            ${stsUPDmute}.
            </h4>
            
    <div class="separator"><hr></div>
HTML
    fi

    ## MPD install check
    ## If the mpd installation is [installed,local],
    ## reinstall mpd so that automatic updates are enabled.

        mpd_Install_CHK=$(sudo apt -a -qq list mpd 2>/dev/null | grep "\[installed,local\]")

        if [ -n "$mpd_Install_CHK" ]; then
            sudo apt —reinstall -y install mpd 2>/dev/null
        fi
    ##

######## RaspberryPi OS Update

stsUPD=$(sudo apt update -qq 2>/dev/null | cut -d"." -f 1)
lastUPD=$(sudo sed -n '$p' /var/www/cgi-bin/log/update.log)
apt_list=$(sudo apt list --upgradable -qq 2>/dev/null | sed -e "s/$/<br>/g")

    if [ "$stsUPD" = "All packages are up to date" ]; then

        cat <<HTML
        <!-- RaspberryPi OS -->
        <div class="title-btn-title">
          <a href="" class="toggle-off-sw"> Update </a>
          <h3>RaspberryPi OS</h3>
        </div>

            <h4>
            Last Updated : ${lastUPD:- Not updated yet}</br>
            ${stsUPD}.
            </h4>
HTML
    else

        cat <<HTML
        <!-- RaspberryPi OS Update Available-->
        <div class="title-btn-title">
          <a href="#" onClick="dispUpdate(); return false;" target="_self" class="toggle-on-sw"> Update </a>
          <h3>RaspberryPi OS</h3>
          <div class="status">Update Available</div>
        </div>

            <h4>
            Last Updated : ${lastUPD:- Not updated yet}</br>
            ${stsUPD}.
            </h4>
            
            <h4>
            ${apt_list}
            </h4>
HTML
    fi

    cat <<HTML
    <div class="separator"><hr></div>
    </body>
</html>
HTML
