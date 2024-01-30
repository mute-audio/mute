#!/bin/bash

# index.cgi                                        #
# (C)2024 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)
muteLogo=$(< /var/www/html/image/mute_logo.svg)

cat << HTML
Content-type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
  <head>

   <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
   <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
   <meta name="mobile-web-app-capable" content="yes">
   <meta http-equiv="Cache-Control" content="no-cache">

   <title>[ mute ]</title>
   <link rel="stylesheet" type="text/css" href="/css/main.css?$query">
   <link rel="icon" type="image/png" href="/image/mute_favicon.png">
   <link rel="apple-touch-icon" href="/image/mute_apple_icon.png">

  </head>

  <body>

    <!-- Main Page -->
    <div id="splitView">

      <!-- Side Bar Lock -->
      <div id="sidebar" class="sidebar-ui-unlock">
      </div>

      <!-- Side Bar Menu -->
      <div class="sidebar">

        <!-- mute logo, reload -->
        <div>
          <a href="#" onClick="location.reload(); return false;" target="_self">
          <div class="icon">${muteLogo}</div>
          </a>
        </div>

        <!-- RaspberryPi -->
        <form method=GET action="/cgi-bin/loading.cgi" target="mainview">
          <input type="hidden" name="URL" value="/cgi-bin/RaspberryPi/Raspberrypi.cgi">
          <input id="Raspberrypi" type="submit" value="RaspberryPi" class="menutab">
          <div id="RaspberrypiBadge" class="status-min" style="display: none;"> </div>
        </form>

        <!-- Sound Device -->
        <form method=GET action="/cgi-bin/loading.cgi" target="mainview">
          <input type="hidden" name="URL" value="/cgi-bin/Sound_Device/Sound_device.cgi">
          <input id="SoundDevice" type="submit" value="Sound Device" class="menutab">
        </form>

        <!-- Source Volume -->
        <form method=GET action="/cgi-bin/loading.cgi" target="mainview">
          <input type="hidden" name="URL" value="/cgi-bin/Source_Volume/Source_volume.cgi">
          <input id="SourceVolume" type="submit" value="Source Volume" class="menutab">
        </form>

        <!-- MPD -->
        <form method=GET action="/cgi-bin/loading.cgi" target="mainview">
          <input type="hidden" name="URL" value="/cgi-bin/MPD/check_MPD.cgi">
          <input id="MPD" type="submit" value="MPD" class="menutab">
        </form>

        <!-- Other Settings -->
        <form method=GET action="/cgi-bin/loading.cgi" target="mainview">
          <input type="hidden" name="URL" value="/cgi-bin/Other_Settings/Other_setting.cgi">
          <input id="OtherSettings" type="submit" value="Other Settings" class="menutab">
        </form>

        <!-- Update -->
        <form method=GET action="/cgi-bin/Checking.cgi" target="mainview">
          <input type="hidden" name="URL" value="/cgi-bin/Update/Update.cgi">
          <input id="Update" type="submit" value="Update" class="menutab">
          <div id="UpdateBadge" class="status-min" style="display: none;"> </div>
        </form>

        <!-- About [ mute ] -->
        <form method=GET action="/cgi-bin/loading.cgi" target="mainview">
          <input type="hidden" name="URL" value="/cgi-bin/About/about_mute.cgi">
          <input id="AboutMute" type="submit" value="About [ mute ]" class="menutab">
        </form>

      </div>

      <!-- Main View -->
      <div class="main">
        <iframe src="/cgi-bin/start.cgi" name="mainview"></iframe>
      </div>

    </div>

    <script>

        function setUpdateBadge() {
            const UpdateBadge = document.querySelector('#UpdateBadge');

            fetch("/cgi-bin/Update/Update_notice.txt")
            .then(response => response.text())
            .then((text) => {
              if( text === 'All packages are up to date.\n'){
                UpdateBadge.style.display = 'none';
              }else{
                UpdateBadge.style.display = '';
              }
            })
            .catch((error) => console.log(error))

            setTimeout( setUpdateBadge , 10000 )
        }

        setUpdateBadge();

    </script>

  </body>
</html>
HTML
