#!/bin/bash

# other_setting_ip.cgi  						               #
# (C)2023 kitamura_design <kitamura_design@me.com> #

# Get infomations
# mpdscribble
ScrobberSTATUS=$(systemctl status mpdscribble | sed -n 3p | cut -d"(" -f2 | cut -d")" -f1)
CurrentUSER=$(sudo sed -n -e '/\[last.fm\]/,+3p' /etc/mpdscribble.conf | sed -n -e 3P | cut -d " " -f3)
CurrentPWD=$(sudo sed -n -e '/\[last.fm\]/,+3p' /etc/mpdscribble.conf | sed -n -e 4P | cut -d " " -f3)

if [ "$ScrobberSTATUS" = "running" ]; then

 ScrSTATUS=Running
 ScrSW="Stop"
 ScrCGI=mpdscribble_stop.cgi

else

 ScrSTATUS=Stopped
 ScrSW=Start
 ScrCGI=mpdscribble_restart.cgi

fi

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="/css/main.css?$query">
    <script src="/dist/clipboard.js"></script>
    <script>
      function keepHover(){
        target = parent.document.getElementById("OtherSettings");
        if (target != null){
            target.className = "menutab-keephover";
        }
      }

      function offHover(){
        target = parent.document.getElementById("OtherSettings");
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

    <body id="iframe" onLoad="keepHover()" onunload="offHover()">

    <h1>Other Settings</h1>

        <!-- LastFM  mpdscribble -->
        <h3>LastFM Scrobbler</h3>
          <div class="setting-items-wrap">
             <a href="/cgi-bin/Other_Settings/mpdscribble_processing.cgi?${ScrCGI}" target="_self" class="button"> ${ScrSW} </a>
             <input value="${CurrentUSER:-"( Not Assigned )"}" class="inputbox-single-readonly" readonly>
             <label><div class="status">${ScrSTATUS}</div></label>
          </div>

            <!-- Account Setting -->
            <h4> Account Setting </h4>
            <form method=GET action="/cgi-bin/Other_Settings/submitting_SCRIBBLE.cgi" target="_self">
                <ul>
                <!-- User -->
                <li class="setting-items-wrap">
                  <div class="ellipsis-wrap">Aa</div>
                  <input type="text" id="user" name="user"  placeholder="User" class="inputbox" required>
                  <label for="">User</label>
                </li>

                <!-- Password -->
                <li class="setting-items-wrap">
                  <div class="ellipsis-wrap">Aa</div>
                  <input type="password" id="password" name="password" placeholder="Password" class="inputbox" required>
                  <label for="">Password</label>
                </li>
                </ul>

                <!-- Submit & reset -->
                <div class="setting-items-wrap">
                  <input id="login" type="submit" value=" Submit " class="button"></input>
                  <input id="reset" type="reset" value=" Reset " class="button2"></input>
                </div>
            </form>

        <div class="separator"><hr></div>

        <!-- Getcover -->
        <h3>Generate Coverart File ( supports FLAC, ALAC, and AAC )</h3>

          <form method=GET action="/cgi-bin/Other_Settings/getcover_processing.cgi" target="_self">
            <div class="setting-items-wrap">
              <input type="submit" value=" Generate " class="button">
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select id="filename" name="filename" class="inputbox-single">
              <option value="Folder" selected>Folder.jpg</option>
              <option value="Cover">Cover.jpg</option>
              </select>
              <label>File Name</label>
            </div>
          </form>

        <div class="separator"><hr></div>

        <!-- MPD Client Information -->
        <div class="title-btn-title">
          <a href="/cgi-bin/Other_Settings/other_setting_host.cgi" target="_self" class="toggle-on-sw">By Host</a>
          <h3>MPD Client Information</h3>
        </div>

            <!-- MPD Server -->
            <div class="setting-items-wrap">
            <button class="btn" data-clipboard-target="#MPD-ip">Copy</button>
            <input id="MPD-ip" value="$(hostname -I | cut -d " " -f 1)" class="inputbox-single-readonly" readonly></input>
            <label>MPD Server</label>
            </div>
            <!-- Coverart URL -->
            <div class="setting-items-wrap">
            <button class="btn" data-clipboard-target="#COVER-ip">Copy</button>
            <input id="COVER-ip" value="http://$(hostname -I | cut -d " " -f 1)/music" class="inputbox-single-readonly" readonly></input>
            <label>Coverart URL</label>
            </div>

        <div class="separator"><hr></div>
HTML

### User Interface ###

        cat <<HTML
        <h3>User Interface</h3>
HTML

    ### Dark Mode Setting ####
    darkmodeSTS=$(grep darkmode /var/www/cgi-bin/etc/mute.conf)

       if [ "$darkmodeSTS" = "darkmode=on" ]; then
       cat <<HTML
        <!-- Dark Mode Selector -->

          <form method=GET action="/cgi-bin/Other_Settings/darkmode_sw_Processing.cgi" target="_parent">
            <div class="setting-items-wrap">
              <input type="submit" value=" Apply " class="button">
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select id="theme" name="theme" class="inputbox-single">
                <option value="darkmode=on" selected >Dark Mode</option>
                <option value="darkmode=off">Light Mode</option>
                <option value="darkmode=auto">Auto (System)</option>
              </select>
              <label>Dark / Light Mode</label>
            </div>
          </form>
HTML

       elif [ "$darkmodeSTS" = "darkmode=off" ]; then
       cat <<HTML
        <!-- Dark Mode Selector -->

          <form method=GET action="/cgi-bin/Other_Settings/darkmode_sw_Processing.cgi" target="_parent">
            <div class="setting-items-wrap">
              <input type="submit" value=" Apply " class="button">
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select id="theme" name="theme" class="inputbox-single">
                <option value="darkmode=on" >Dark Mode</option>
                <option value="darkmode=off" selected >Light Mode</option>
                <option value="darkmode=auto">Auto (System)</option>
              </select>
              <label>Dark / Light Mode</label>
            </div>
          </form>
HTML

       elif [ "$darkmodeSTS" = "darkmode=auto" ]; then
       cat <<HTML
        <!-- Dark Mode Selector -->

          <form method=GET action="/cgi-bin/Other_Settings/darkmode_sw_Processing.cgi" target="_parent">
            <div class="setting-items-wrap">
              <input type="submit" value=" Apply " class="button">
              <div class="ellipsis-wrap"><div class="allow-down"></div></div>
              <select id="theme" name="theme" class="inputbox-single">
                <option value="darkmode=on" >Dark Mode</option>
                <option value="darkmode=off">Light Mode</option>
                <option value="darkmode=auto" selected >Auto (System)</option>
              </select>
              <label>Dark / Light Mode</label>

            </div>
          </form>
HTML
      fi

        ### System Startup Sound  ####

      if [[ -L /etc/systemd/system/multi-user.target.wants/startUpSound.service ]]; then

        cat <<HTML
        <div class="setting-items-wrap">
         <div class="toggle-wrap">
            <a id="SoundOFFbtn" href="/cgi-bin/Other_Settings/StartUpSound_switching.cgi?other_setting_ip.cgi" onclick="toggleOff()" target="_self" class="toggle-on-sw"> Enabled </a>
            <div class="toggle-on-wrap"><div id="tgl-on" class="toggle-on-mark"></div></div>
            </div><input class="inputbox-single-invisible" value="off/any  " readonly="">
            <label>System Startup Sound</label>
        </div>
HTML
      else

        cat <<HTML
        <div class="setting-items-wrap">
         <div class="toggle-wrap">
            <div class="toggle-off-wrap"><div id="tgl-off" class="toggle-off-mark"></div></div>
            <a id="SoundONbtn" href="/cgi-bin/Other_Settings/StartUpSound_switching.cgi?other_setting_ip.cgi" onclick="toggleOn()" target="_self" class="toggle-off-sw"> Disabled </a>
            </div><input class="inputbox-single-invisible" value="off/any  " readonly="">
            <label>System Startup Sound</label>
        </div>
HTML
      fi

### Clipboard.js ####
        cat <<HTML
        <div class="separator"><hr></div>

        <script>
          var cp = new ClipboardJS('.btn');
          cp.on("success", function(e) {
              alert( 'Copied.' ) ;
              } ) ;
        </script>

    </body>
</html>
HTML
