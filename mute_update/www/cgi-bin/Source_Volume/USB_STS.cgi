#!/bin/bash

# USB_STS.cgi                              #
# (C)2023 kitamura_design <kitamura_design@me.com> #

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

exit 0