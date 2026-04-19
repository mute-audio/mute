#!/bin/bash

# DLNA_AirPlay.cgi                                 #
# (C)2026 kitamura_design <kitamura_design@me.com> #


cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
        <head>
          <link rel="stylesheet" type="text/css" href="/css/main.css">
          <script>

    	    function autoRebootMsg(){
      		if(window.confirm('Automatically Reboot after running.\nAre you sure?')){
	     		return true;
		    } else {
		        return false;
		    }
		 }

            function keepHover(){
                target = parent.document.getElementById("DLNA-AirPlay");
                if (target != null){
                        target.className = "menutab-keephover";
                        }
                }

            function offHover(){
                target = parent.document.getElementById("DLNA-AirPlay");
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
	<body id="iframe" onLoad="keepHover()" onunload="offHover()">

		<h1>DLNA / AirPlay</h1>
HTML

## DLNA Status & Change Name
DLNA_STATUS=$(sudo systemctl is-enabled upmpdcli 2>/dev/null)
# Extract name from -f "[name]" in systemd service file
DLNA_NAME=$(grep "^avfriendlyname" /etc/upmpdcli.conf | sed -e 's|avfriendlyname = ||')


if [ ${DLNA_STATUS} = "enabled" ]; then

cat <<HTML
		<!-- DLNA toggle enabled -->
		<div class="title-btn-title">
		  <div class="toggle-wrap" style="float: right;">
		     <a id="dlna_btn" href="/cgi-bin/DLNA_AirPlay/Toggling_DLNA.cgi" onClick="toggleOff()" target="mainview" class="toggle-on-sw"> ${DLNA_STATUS^} </a>
		     <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
		  </div>
		  <h3>DLNA : UpMPDcli</h3><label>
		</div>
HTML

else
cat <<HTML
      <!-- DLNA toggle disabled -->
      <div class="title-btn-title">
        <div class="toggle-wrap" style="float: right;">
            <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
            <a id="dlna_btn" href="/cgi-bin/DLNA_AirPlay/Toggling_DLNA.cgi" onClick="toggleOn()" target="mainview" class="toggle-off-sw"> ${DLNA_STATUS^} </a>
        </div>
        <h3>DLNA : UpMPDcli</h3><label>
      </div>
HTML
fi

cat <<HTML
		<!-- Name Setting -->
		<h4> Display Name Setting </h4>
                <form method=GET action="/cgi-bin/DLNA_AirPlay/Renaming_DLNA.cgi" onsubmit="" target="_self">
                        <div class="setting-items-wrap">
                            <input id="dlna_Apply" type="submit" value="Set" class="button"></input>
                            <div class="ellipsis-wrap">Aa</div>
                            <input type="text" id="dlnaNAME" name="dlnaNAME" value="$DLNA_NAME" class="inputbox-single" required>
                            <label for="">Name</label>
                        </div>
                </form>

            <div class="separator"><hr></div>
            <div class="separator"><hr></div>
HTML

## AirPlay Status & Setting
AirPlay_STATUS=$(sudo systemctl is-enabled shairport-sync 2>/dev/null)
# Extract name from name = "[name]"; in config file
AirPlay_NAME=$(grep -E '^[[:space:]]*name =' /etc/shairport-sync.conf | head -n 1 | cut -d'"' -f2)

if [ ${AirPlay_STATUS} = "enabled" ]; then

cat <<HTML
                <!-- AirPlay toggle -->
                <div class="title-btn-title">
                  <div class="toggle-wrap" style="float: right;">
                     <a id="airplay_btn" href="/cgi-bin/DLNA_AirPlay/Toggling_AirPlay.cgi" onClick="toggleOff()" target="mainview" class="toggle-on-sw"> ${AirPlay_STATUS^} </a>
                     <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
                  </div>
                  <h3>AirPlay : Shairport Sync</h3><label>
                </div>
HTML

else

cat <<HTML
                <!-- AirPlay toggle -->
                <div class="title-btn-title">
                  <div class="toggle-wrap" style="float: right;">
                     <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
                     <a id="airplay_btn" href="/cgi-bin/DLNA_AirPlay/Toggling_AirPlay.cgi" onClick="toggleOn()" target="mainview" class="toggle-off-sw"> ${AirPlay_STATUS^} </a>
                  </div>
                  <h3>AirPlay : Shairport Sync</h3><label>
                </div>
HTML
fi

cat <<HTML
            <!-- Name Setting -->
		<h4>Display Name Setting</h4>
		<form method=GET action="/cgi-bin/DLNA_AirPlay/Renaming_AirPlay.cgi" onsubmit="" target="_self">
			<div class="setting-items-wrap">
			    <input id="airplay_Apply" type="submit" value="Set" class="button"></input>
			    <div class="ellipsis-wrap">Aa</div>
			    <input type="text" id="airplayNAME" name="airplayNAME" value="$AirPlay_NAME" class="inputbox-single" required>
			    <label for="">Name</label>
			</div>
		</form>

	<script>
  </script>

       </body>
</html>
HTML
