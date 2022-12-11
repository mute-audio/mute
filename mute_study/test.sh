#!/bin/bash

cat << -RaspberryPi-
<html>
    <body>
        <div>
          <a>
          </a>
        </div>
    </body>
</html>
-RaspberryPi-

cat <<--RaspberryPi-
    <html>
        <body>
            <div>
             <a>
             </a>
            </div>
        </body>
    </html>
-RaspberryPi-

#WiFi AP Scan One-liner
sudo iwlist wlan0 scan | grep ESSID | sort | uniq | cut -d "\"" -f 2

#WiFi AP Scan function
wifi_ap_scan() {
    sudo iwlist wlan0 scan \
    | grep ESSID | sort | uniq \
    | cut -d "\"" -f 2
}

