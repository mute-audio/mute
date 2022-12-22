#!/bin/bash

# Source_volume.cgi                              #
# (C)2022 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

cat <<HTML
<!-- HTML Header -->
Content-type: text/html; charset=utf-8"

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
        </script>
        </head>
HTML
      cat <<HTML
        <body id="iframe" onLoad="keepHover()" onunload="offHover()">

        <!-- Title-->
        <h1>Source Volume</h1>
HTML

 #### NAS List (Multiple Version)
 NAS_count=$(df -ah | grep -c /mnt.*) # Check NAS

      if [ $NAS_count = 0 ]; then
        cat <<HTML
        <h3>NAS</h3>
        <div class="setting-items-wrap">
          <a class="button-disabled">Unmount</a>
          <input class="inputbox-single-readonly" value="-- No NAS Mounted --" readonly>
        </div>
HTML
      else

         for ((i=1; i<=$NAS_count; i++)); do

            NAS=$(df -ah | grep /mnt.* | cut -d " " -f 1 | sed -n "$i"p) ## Get NAS Volume
            NAS_name=$(df -ah | grep --only-matching /mnt.* | sed -n "$i"p) ##Get NAS Name
            busyCHECK=$(sudo lsof "$NAS_name")

            if [ -n "$busyCHECK" ]; then

             nasSTS='Busy'  #Set Disable un-mount

             cat <<HTML
              <h3>NAS</h3>
              <div class="setting-items-wrap">
                <a class="button-disabled">Unmount</a>
                <input class="inputbox-single-readonly" value="${NAS_name} : ${NAS}" readonly>
                <label><div id="nasSTS" class="status">${nasSTS}</div></label>
              </div>
HTML
            else

             nasSTS='Not busy' #Set Enable un-mount

             cat <<HTML
              <h3>NAS</h3>
              <div class="setting-items-wrap">
                <a href="/cgi-bin/Source_Volume/unmounting_NAS.cgi?${NAS_name}" target="_self" class="button">Unmount</a>
                <input class="inputbox-single-readonly" value="${NAS_name} : ${NAS}" readonly>
              <label><div id="nasSTS" class="status">${nasSTS}</div></label>
              </div>
HTML
            fi

         done

      fi

 #### NAS Mount Form
 busyCHECK2=$(sudo lsof /mnt/*)

      if [ -n "$busyCHECK2" ]; then

        cat <<HTML
        <h4> NAS Setting [ SMB ] -- Disabled while Busy --</h4>

        <form method=GET action="/cgi-bin/Source_Volume/mount_NAS.cgi" target="_self">
             <ul>
                  <!-- NAS Label (Mount Name) -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="mount_name" name="mount_name" placeholder="NAS_1" class="inputbox" disabled>
                   <label for="">NAS Name</label>
                </li>

                  <!-- Volume Path -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="volume_path" name="volume_path" placeholder="192.168.xx.xxx/share/music" class="inputbox" disabled>
                   <label for="">Volume Path</label>
                </li>

                  <!-- smb option -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="vers" name="vers" placeholder="vers=1.0" class="inputbox" disabled>
                   <label for="">SMB Version</label>
                </li>

                  <!-- User -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="user" name="user" placeholder="User Name" class="inputbox" disabled>
                   <label for="">User</label>
                </li>

                  <!-- Password -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="password" id="password" name="password" placeholder="Password" class="inputbox" disabled>
                   <label for="password">Password</label>
                </li>
             </ul>

             <!-- Submit & reset -->
             <div class="setting-items-wrap">
             <input id="submit" type="submit" value=" Mount " class="button-disabled" disabled></input>
             <input id="reset" type="reset" value=" Reset " class="button2" disabled></input>
             </div>
        </form>
HTML
      else

        cat <<HTML
        <h4> NAS Setting [ SMB ]</h4>

        <form method=GET action="/cgi-bin/Source_Volume/mouting_NAS.cgi" target="_self">
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
HTML
      fi


 #### USB Drive List
 USB_count=$(df -h | grep /media/ | cut -d "/" -f 5 | wc -l)

      if [ $USB_count = 0 ]; then

        cat <<HTML
        <h3>USB</h3>

        <div class="setting-items-wrap">
        <a class="button-disabled">Unmount</a>
        <input class="inputbox-single-readonly" value="-- No USB Drive --" readonly>
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
             <!-- Title -->
             <h3>USB</h3>

              <div class="setting-items-wrap">
                   <a class="button-disabled">Unmount</a>
                   <input class="inputbox-single-readonly" value="/media/${LABEL}" readonly>
                   <label><div id="usbSTS" class="status">${usbSTS}</div></label>
              </div>
HTML
            else
             usbSTS="Not Busy"

              cat <<HTML
             <!-- Title -->
             <h3>USB</h3>

              <div class="setting-items-wrap">
                   <a href="/cgi-bin/Source_Volume/unmounting_USB.cgi?${USB}" target="_self" class="button">Unmount</a>
                   <input class="inputbox-single-readonly" value="/media/${LABEL}" readonly>
                   <label><div id="usbSTS"class="status">${usbSTS}</div></label>
              </div>
HTML
            fi

        done

      fi
      cat <<HTML

              <div class="separator"><hr></div>

       </body>
</html>
HTML
