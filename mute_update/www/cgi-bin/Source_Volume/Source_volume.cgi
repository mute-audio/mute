#!/bin/bash

# Source_volume.cgi                              #
# (C)2024 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
       <head>
        <link rel="stylesheet" type="text/css" href="/css/main.css?$query">
        <script>

          function keepHover(){
              target = parent.document.getElementById("SourceVolume");
              if (target != null){
                  target.className = "menutab-keephover";
              }
          }

          function offHover(){
              target = parent.document.getElementById("SourceVolume");
              if (target != null){
                  target.className = "menutab";
                  }
          }

          function dbUpdateMsg(){
              if(window.confirm('After mounting, DB Update in the MPD menu.')){
              return true;
              } else {
              return false;
              }
          }

        </script>
        </head>
HTML
      cat <<HTML
        <body id="iframe" onLoad="keepHover()" onunload="offHover()">

        <!-- Title-->
        <h1>Source Volume</h1>
HTML

 #### NAS List (Multiple Version)

        cat <<HTML
        <h3>NAS</h3>
        <div id="NAS_list">
HTML

 NAS_count=$(df -ah | grep -c /mnt.*) # Check NAS

      if [ $NAS_count = 0 ]; then
        cat <<HTML
        <div class="setting-items-wrap">
          <a class="button-disabled">Unmount</a>
          <input class="inputbox-single-readonly" value="-- No NAS Mounted --" readonly>
          <label><div class="status" style="display: none;">none</div></label>
        </div>
HTML
      else

         for ((i=1; i<=$NAS_count; i++)); do

            NAS=$(df -ah | grep /mnt.* | cut -d " " -f 1 | sed -n "$i"p) ## Get NAS Volume
            NAS_name=$(df -ah | grep --only-matching /mnt.* | sed -n "$i"p | sed -e "s/\/.*\///") ##Get NAS Name
            busyCHECK=$(sudo lsof "/mnt/${NAS_name}")

            if [ -n "$busyCHECK" ]; then

             nasSTS='Busy'  #Set Disable un-mount

             cat <<HTML
              <div id="nas-$i"class="setting-items-wrap">
                <a class="button-disabled">Unmount</a>
                <input class="inputbox-single-readonly" value="${NAS_name} : ${NAS}" readonly>
                <label><div class="status">${nasSTS}</div></label>
              </div>
HTML
            else

             nasSTS='Not busy' #Set Enable un-mount

             cat <<HTML
              <div id="nas-$i" class="setting-items-wrap">
                <a href="/cgi-bin/Source_Volume/unmounting_NAS.cgi?${NAS_name}" target="_self" class="button">Unmount</a>
                <input class="inputbox-single-readonly" value="${NAS_name} : ${NAS}" readonly>
              <label><div class="status">${nasSTS}</div></label>
              </div>
HTML
            fi

         done

      fi

      cat <<HTML
      </div>
HTML

 #### NAS Mount Form
        cat <<HTML
        <div id="NAS_MOUNT_FORM">
        <h4> NAS Setting [ SMB ]</h4>

        <form method=GET action="/cgi-bin/Source_Volume/mouting_NAS.cgi" onsubmit="return dbUpdateMsg()" target="_self">
             <ul>
                  <!-- NAS Label (Mount Name) -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="mount_name" name="mount_name" placeholder="NAS_1" class="inputbox" required>
                   <label for="">NAS Name</label>
                </li>

                  <!-- Volume Path -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="volume_path" name="volume_path" placeholder="192.168.xx.xxx/share/music" class="inputbox" required>
                   <label for="">Volume Path</label>
                </li>

                  <!-- smb option -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="vers" name="vers" placeholder="vers=1.0" class="inputbox">
                   <label for="">SMB Version</label>
                </li>

                  <!-- User -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="user" name="user" placeholder="User Name" class="inputbox">
                   <label for="">User</label>
                </li>

                  <!-- Password -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="password" id="password" name="password" placeholder="Password" class="inputbox">
                   <label for="">Password</label>
                </li>
             </ul>

             <!-- Submit & reset -->
             <div class="setting-items-wrap">
             <input id="submit" type="submit" value=" Mount " class="button"></input>
             <input id="reset" type="reset" value=" Reset " class="button2"></input>
             </div>
        </form>
      </div>
HTML


 #### USB Drive List
        cat <<HTML
        <h3>USB</h3>
        <div id="USB_list">
HTML

 USB_count=$(df -h | grep /media/ | cut -d "/" -f 5 | wc -l)

      if [ $USB_count = 0 ]; then

        cat <<HTML
        <div class="setting-items-wrap">
        <a class="button-disabled">Unmount</a>
        <input class="inputbox-single-readonly" value="-- No USB Drive --" readonly>
        <label><div class="status" style="display: none;">none</div></label>
        </div>
HTML
      else

        for ((i=1; i<=$USB_count; i++)); do

        USB=$(df -h | grep /media/ | cut -d "/" -f 5 | sed -n "$i"p)
        LABEL=$(sudo lsblk -f -oLABEL -n /dev/"$USB")
        busyCHECK_USB=$(sudo lsof /media/"$USB")

            if [ -n "$busyCHECK_USB" ]; then
             usbSTS="Busy"

              cat <<HTML
              <div id="usb-$i" class="setting-items-wrap">
                   <a class="button-disabled">Unmount</a>
                   <input class="inputbox-single-readonly" value="${LABEL}" readonly>
                   <label><div class="status">${usbSTS}</div></label>
              </div>
HTML
            else
             usbSTS="Not Busy"

              cat <<HTML
              <div id="usb-$i" class="setting-items-wrap">
                   <a href="/cgi-bin/Source_Volume/unmounting_USB.cgi?${USB}" target="_self" class="button">Unmount</a>
                   <input class="inputbox-single-readonly" value="${LABEL}" readonly>
                   <label><div class="status">${usbSTS}</div></label>
              </div>
HTML
            fi

        done

      fi

        cat <<HTML
        </div>
HTML

      cat <<HTML

              <div class="separator"><hr></div>
        
        <script>

        function nasSTSCheck() {
                   const nasList = document.querySelector("#NAS_list");
                   const URL = '/cgi-bin/Source_Volume/NAS_STS.cgi';

                    fetch(URL)
                    .then( (response) => response.text() )
                    .then( (text) => nasList.innerHTML = text )
                    .catch( (error) => console.log(error) )

                 setTimeout( nasSTSCheck , 5000 );
        }

        nasSTSCheck();


        function usbSTSCheck() {
                   const usbList = document.querySelector("#USB_list");
                   const URL = '/cgi-bin/Source_Volume/USB_STS.cgi';

                    fetch(URL)
                    .then( (response) => response.text() )
                    .then( (text) => usbList.innerHTML = text )
                    .catch( (error) => console.log(error) )

                 setTimeout( usbSTSCheck , 5000 );
        }

        usbSTSCheck();

        </script>

       </body>
</html>
HTML
