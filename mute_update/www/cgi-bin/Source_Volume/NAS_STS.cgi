#!/bin/bash

# NAS_STS.cgi                              #
# (C)2023 kitamura_design <kitamura_design@me.com> #

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
            busyCHECK=$(sudo lsof "$NAS_name")

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

exit 0