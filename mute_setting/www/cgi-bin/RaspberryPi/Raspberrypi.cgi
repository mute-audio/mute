#!/bin/bash

# Raspberrypi.cgi		        				   #
# (C)2024 kitamura_design <kitamura_design@me.com> #

#### HTML Header
query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
	<head>
		<link rel="stylesheet" type="text/css" href="/css/main.css?$query">
		<!-- <meta http-equiv="Refresh" content="60"> -->

		<script type="text/javascript">

		  function dispReboot(){
				if(window.confirm('Are you sure to Reboot?')){
					location.href = "/cgi-bin/RaspberryPi/rebooting.cgi";
				}
			}

		  function dispPoweroff(){
				if(window.confirm('Are you sure to Poweroff?')){
					location.href = "/cgi-bin/RaspberryPi/shutting_down.cgi";
				}
			}

		  function disp64bit(){
				if(window.confirm('Automatically Reboot after running.\nAre you sure?')){
					location.href = "/cgi-bin/RaspberryPi/64bit_Processing.cgi?64bit_SW.cgi";
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
				target = parent.document.getElementById("Raspberrypi");
				if (target != null){
					target.className = "menutab-keephover";
				}
			}

		  function offHover(){
				target = parent.document.getElementById("Raspberrypi");
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

		<h1>RaspberryPi</h1>
HTML

#### MainBoard status: CPU Model, Vendor, RAM, and Temp
mainboard=$(grep Model /proc/cpuinfo | cut -d ":" -f 2 | sed -e 's/^ //g')
#temp="$(cat /sys/class/thermal/thermal_zone0/temp)"
#TEMP="$(bc <<< "scale=1; $temp/1000") c˚"
TEMP=$(sudo vcgencmd measure_temp | cut -d "=" -f 2)
CPUMax=$(sudo vcgencmd get_config int | grep arm_freq | cut -d "=" -f 2 | sed -n 1p)
VNDR=$(sudo lscpu | grep Vendor | cut -d ":" -f 2 | cut -d " " -f 12)
MDL=$(sudo lscpu | grep "Model name" | cut -d ":" -f 2 | sed -e 's/ //g')
RAM=$(free --mega -t | grep Total: | sed -e 's/  */ /g' | cut -d " " -f2)

cat <<HTML
		<!-- Main Board -->
		<div class="title-btn-title">
			<!-- Poweroff Button -->
			<a href="#" onClick="dispPoweroff(); return false;" target="_self" class="toggle-on-sw"> Poweroff </a>
			<h3>Main Board : ${mainboard}</h3>
		</div>
			<!-- Main Board Info-->
			<h4>
			${VNDR} ${MDL} / ${CPUMax} MHz / ${RAM} MB RAM
			<br>
			<div id="temp">CPU Temp : ${TEMP}</div>
			</h4>
		<div class="separator"><hr></div>
HTML

######## RaspberryPi OS
DISTRO=$(lsb_release -a 2>/dev/null | sed -n 2p | cut -d "(" -f 2 | cut -d ")" -f 1)
kernelR=$(uname -r)
kernelNAME=$(uname -s)

if [ -e "/var/www/cgi-bin/log/reboot_required.log" ]; then
	reboot_badge="<div class="status">Reboot required</div>"
fi

cat <<HTML
		<!-- RaspberryPi OS -->
		<div class="title-btn-title">
			<!-- Reboot Button -->
			<a href="#" onClick="dispReboot(); return false;" target="_self" class="toggle-on-sw"> Reboot </a>
			<h3>OS : RaspberryPi OS ${DISTRO^}</h3>
			${reboot_badge}
		</div>
			<!-- RaspberryPi OS Info -->
			<!-- h4>Kernel : ${kernelNAME} ${kernelR}</h4 -->
HTML

######### Genaral Options: TimeZone
#TimezoneSTS=$(< /etc/timezone)
TimezoneSTS=$(timedatectl show | grep Timezone | cut -d "=" -f 2)
TimezoneLIST=$(timedatectl list-timezones | sed -e 's/^/<option>/g' -e 's/$/<\/option>/g')

cat <<HTML
		<!-- General Options -->
		<h4>General Options</h4>

			<!-- Host Name Change:text-input -->
			<form method=GET action="/cgi-bin/RaspberryPi/host_name_change_processing.cgi" onsubmit="return autoRebootMsg()" target="_self">
			    <div class="setting-items-wrap">
				  <input id="Apply" type="submit" value="Set" class="button"></input>
				  <div class="ellipsis-wrap">Aa</div>
				  <input type="text" id="hostNAME" name="hostNAME" value="$(hostname)" class="inputbox-single" required>
				  <label for="">Hostname</label>
			    </div>
			</form>

			<!-- Host Password Change:text-input -->
			<form method=GET action="/cgi-bin/RaspberryPi/host_pwd_change_processing.cgi" onsubmit="return autoRebootMsg()" target="_self">
				<div class="setting-items-wrap">
				  <input id="Apply" type="submit" value="Set" class="button"></input>
				  <div class="ellipsis-wrap">Aa</div>
				  <input type="password" id="hostPWD" name="hostPWD" value="" class="inputbox-single" placeholder="Password" required>
				  <label for="">Password</label>
				</div>
			</form>

			<!-- Timezone: pull-down list -->
			<form method=GET action="/cgi-bin/RaspberryPi/timezone_processing.cgi" target="_self">
				<div class="setting-items-wrap">
				  <input type="submit" value=" Apply " class="button">
				  <div class="ellipsis-wrap"><div class="allow-down"></div></div>
				  <select id="timezone" name="timezone" class="inputbox-single">
				     <option selected disabled>${TimezoneSTS}</option>
				     ${TimezoneLIST}
				  </select>
				  <label>Timezone</label>
				</div>
			</form>
HTML

#### Bonjour/ Avahi
SOCKET=$(systemctl status mpd.socket | sed -n 3p | cut -d"(" -f2 | cut -d")" -f1) # Get the status of mpd.socket

if [ "$SOCKET" = "dead" ]; then 	# If mpd.socket is dead,

  cat <<HTML
		<!-- Bonjour/ Avahi: Enabled-->
		<div class="setting-items-wrap">
		  <div class="toggle-wrap">
		     <a id="avahi_btn" href="/cgi-bin/RaspberryPi/Avahi_Processing.cgi?restart_mpdsocket.cgi" onClick="toggleOff()" target="mainview" class="toggle-on-sw"> Enabled </a>
		     <div class="toggle-on-wrap"><div class="toggle-on-mark"></div></div>
		  </div>
		  <input class="inputbox-single-invisible" value="Enabled" readonly></input>
		  <label>Bonjour / Avahi</label>
		</div>
HTML

else # If mpd.socket is active,

  cat <<HTML
		<!-- Bonjour/ Avahi: Disabled -->
		<div class="setting-items-wrap">
		  <div class="toggle-wrap">
		     <div class="toggle-off-wrap"><div class="toggle-off-mark"></div></div>
		     <a id="avahi_btn" href="/cgi-bin/RaspberryPi/Avahi_Processing.cgi?disable_mpdsocket.cgi" onClick="toggleOn()" target="mainview" class="toggle-off-sw"> Disabled </a>
		  </div>
		  <input class="inputbox-single-invisible" value="disabled" readonly></input>
		  <label>Bonjour / Avahi</label>
		</div>
HTML

fi

#### WiFi Settings

# Initialize wpa_supplicant.conf
wpa_country=$(sudo grep country /etc/wpa_supplicant/wpa_supplicant.conf)
if [ -z ${wpa_country} ]; then
	sudo sed -i -e '$a\\ncountry\=GB' /etc/wpa_supplicant/wpa_supplicant.conf
fi

wpa_network=$(sudo grep network /etc/wpa_supplicant/wpa_supplicant.conf)
if [ -z ${wpa_network} ]; then
	sudo sed -i -e '$a\\nnetwork\={' -e '$a\\tssid=\"SSID\"' -e '$a\\tpsk=\"PWD\"\n}' /etc/wpa_supplicant/wpa_supplicant.conf
fi

# Check WiFi status
wifi_STS=$(rfkill list wlan | grep "Soft blocked" | cut -d " " -f 3)

if [ -z ${wifi_STS} ]; then
 #### Hide WiFi Settings
	echo ''

else
 #### Show WiFi Settings
  cat <<HTML
  <h4 id="output">WiFi Settings</h4>
HTML

	#### WiFi Connection

	# Check current OS Codename
	OS_codename=$(lsb_release -a |  grep Codename | cut -f 2)

	if [ ${OS_codename} = "buster" ] || [ ${OS_codename} = "bullseye" ]; then  # In case of Buster, Bullseye etc.

    	ssid_STS=$(iwconfig wlan0 | grep "wlan0" | cut -d ":" -f 2 | cut -d "\"" -f 2)
    	ssid_LIST=$(sudo iwlist wlan0 scan | grep ESSID | sort | uniq | cut -d ":" -f 2 | cut -d "\"" -f 2 | sed -e 's/^/<option>/g' -e 's/$/<\/option>/g')
	else

    	ssid_STS=$(iwconfig wlan0 | grep "wlan0" | cut -d ":" -f 2 | cut -d "\"" -f 2)
    	ssid_LIST=$(nmcli -f SSID device wifi list | sed -e '/SSID/d' | sort | uniq | sed -e 's/^/<option>/g' -e 's/$/<\/option>/g')
	fi

	if [ "$wifi_STS" = "no" ]; then

  	  cat <<HTML
		  <!-- WiFi Connection [Enabled]-->
		  <div class="setting-items-wrap">
		     <div class="toggle-wrap">
			     <a id="wifi_btn" href="/cgi-bin/RaspberryPi/blocking_wifi.cgi" onClick="toggleOff()" target="_self" class="toggle-on-sw"> Enabled </a>
			     <div class="toggle-on-wrap"><div id="tgl-on" class="toggle-on-mark"></div></div>
             </div>
			 <input class="inputbox-single-invisible" value="${ssid_STS}" readonly></input>
			 <label>WiFi Connection</label>
		  </div>
HTML
	else

	  cat <<HTML
		  <!-- WiFi Connection [Disabled]-->
		  <div class="setting-items-wrap">
             <div class="toggle-wrap">
			     <div class="toggle-off-wrap"><div id="tgl-off" class="toggle-off-mark"></div></div>
				 <a id="wifibtn" href="/cgi-bin/RaspberryPi/WiFi_switching.cgi" onClick="toggleOn()" target="_self" class="toggle-off-sw"> Disabled </a>
         	 </div>
			 <input class="inputbox-single-invisible" value="${ssid_STS}" readonly></input>
			 <label>WiFi Connection</label>
		  </div>
HTML
	fi

	#### WiFi Country
	country=$(sudo grep country /etc/wpa_supplicant/wpa_supplicant.conf | cut -d '=' -f 2)
	country_STS=$(grep ${country} /usr/share/zoneinfo/iso3166.tab)
	country_LIST=$(< /usr/share/zoneinfo/iso3166.tab sed -e /^#/d -e 's/^/<option>/g' -e 's/$/<\/option>/g')

    if [ "$wifi_STS" = "no" ]; then

		cat <<HTML
		  <!-- WiFi Country -->
		  <form method=GET action="/cgi-bin/RaspberryPi/Country_processing.cgi" target="_self">
		     <div class="setting-items-wrap">
		         <input id="country" type="submit" value="Apply" class="button">
		         <div class="ellipsis-wrap"><div class="allow-down"></div></div>
		         <select name="country" class="inputbox-single">
		             <option selected>${country_STS}</option>
		             ${country_LIST}
		         </select>
		         <label> WiFi Country </label>
		     </div>
		  </form>
HTML
	fi

	#### SSID & PWD
    ip_STS=$(ip a | grep wlan0 | grep -o state.* | cut -d " " -f 2)

	if [ "$wifi_STS" = "no" ]; then

		cat <<HTML
		  <!-- SSID & PWD -->
		  <form method=GET action="/cgi-bin/RaspberryPi/WiFi_applying.cgi" target="_self">
		     <!-- SSID  -->
		     <li class="setting-items-wrap">
				 <div id="progressBadge" class="progress-badge" style="display: none;"> </div>
			     <input id="rescan" type="button" value="Scan" class="button" onClick="ssidRescan()">
			     <div class="ellipsis-wrap"><div class="allow-down"></div></div>
		         <select  id="ssid" name="ssid" class="inputbox-single">
		             <option selected>${ssid_STS:- ( No WiFi connection )}</option>
		             ${ssid_LIST}
		         </select>
    		     <label for=""> SSID </label>
			     <!-- Up/ Down Badge  -->
			     <div class="status-wrap">
    		         <div class="status">${ip_STS}</div>
    		     </div>
			 </li>

			 <!-- Password  -->
			 <div class="setting-items-wrap">
				 <div class="ellipsis-wrap">Aa</div>
				 <input id="pwd" name="pwd" type="password" class="inputbox" placeholder="Password" required>
    			 <label for="">Password </label>
			 </div>

			 <!-- Submit & reset -->
			 <div class="setting-items-wrap">
			     <input id="submit" type="submit" value=" Apply " class="button"></input>
				 <input id="reset" type="reset" value=" Reset " class="button2"></input>
			 </div>
		  </form>
		  </div>
HTML
	fi
fi

## CPU Temp & SSID List updator

cat <<HTML
	  <div class="separator"><hr></div>

	    <script>
		// CPU Temp Updater
            function tempUpdateCheck() {
                const tempUpdate = document.querySelector('#temp');
                fetch("/cgi-bin/RaspberryPi/temp_check.cgi")
                .then(response => {

				if( response.status === 500 ){
                  return tempUpdate.outerHTML;
                }
                  return response.text();
                })
                .then((text) => tempUpdate.outerHTML = text)
                .catch((error) => console.log(error))

                setTimeout( tempUpdateCheck , 10000 )
                }

            tempUpdateCheck();

		// Rescan SSID List
            function ssidRescan() {
                const SSID = document.querySelector('#ssid');
                const progressBadge = document.querySelector('#progressBadge');

                if(!SSID) {
                  return;
                }

                progressBadge.style.display = '';
                SSID.disabled = true;

                fetch("/cgi-bin/RaspberryPi/SSID_STS.cgi")
                .then(response => {
                    return response.text();
                })
                .then((text) => {
                    SSID.outerHTML = text;
                    progressBadge.style.display = 'none';
                })
                .catch((error) => console.log(error))
            }

		// Notification badge checker for RaspberryPi tab
           function setRPiBadge() {
                const RPiBadge = parent.document.querySelector('#RaspberrypiBadge');

                fetch("/cgi-bin/log/reboot_required.log")
                .then(response => {
                    if( !response.ok ){
                    RPiBadge.style.display = 'none';
                }else{
                    RPiBadge.style.display = '';
                }
                })
                .catch((error) => {
                    console.log(error);
                })
            }

            setRPiBadge();

	    </script>

	</body>
</html>
HTML

exit 0