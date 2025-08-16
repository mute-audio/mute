#!/bin/bash

# about_mute.cgi                                        #
# (C)2025 kitamura_design <kitamura_design@me.com>      #

VER=$(grep ver /var/www/cgi-bin/etc/mute.conf | cut -d "=" -f 2)
#install_log=$(sudo cat /var/www/cgi-bin/log/install.log | sed -e "s/$/<br>/g")
query=$(date +%Y%m%d%I%M%S)

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>

  <head>
        <link rel="stylesheet" type="text/css" href="/css/main.css">
        <script>
                function keepHover(){
                        target = parent.document.getElementById("AboutMute");
                        if (target != null){
                                target.className = "menutab-keephover";
                        }
                }

                function offHover(){
                        target = parent.document.getElementById("AboutMute");
                        if (target != null){
                                target.className = "menutab";
                        }
                }
        </script>
  </head>

  <body id="iframe" onLoad="keepHover()" onunload="offHover()">

         <h1>About [ mute ]</h1>

         <h3>A Simple RPi-Audio/ MPD Dashboard [ ver.${VER} ]</h3>
         <br>
         <p class="bodytext2">
         This WebApp is designed ONLY to work to set up the "RPi-Audio Player", NOT to browse / play your music library.
         To control MPD, you can use the Client App ( like <a href="https://www.openaudiolab.com/yampc/" target="_blank">yaMPC</a> ) installed on your mobile or tablet.
         <br>
         This WebAPP is released as "A Freeware" under the MIT License.
         <br>
         </p>

         <br>
         <div class="separator"><hr></div>

         <h2>How to set-up</h2>
         <p class="bodytext2">
         <br>
         It consists of the following five sections, which can be accessed from the menu tabs on the left.
         By setting up a section-by-section, you will be able to build "RPi Audio Player" without any knowledge of terminal or Linux commands.
         </p>

         <br>
         <h3>Step 0 : Choose and install MPD</h3>
         <p class="bodytext2">
         On first launch, MPD is not yet installed, so you will first need to select and install the MPD package.
         Choose the MPD package and install it; "an official" Debian version or an "unofficial" Backports version by the MPD project.
         <br>
         </p>

         <br>
         <h3>Step 1 : RaspberryPi</h3>
         <p class="bodytext2">
         The first step is to configure the basic settings for the RaspberryPi.
         <br>
         Configure the time zone, WiFi, and other settings.
         At the same time, you can check the status of the RaspberryPi board, including its model name, CPU temperature, and RaspberryPi OS version.
         Also refer to this menu when you want to power off or reboot.
         <br>
         </p>

         <br>
         <h3>Step 2 : Sound Device</h3>
         <p class="bodytext2">
         The next step is to configure the sound devices such as the DAC HAT and USB DAC.
         <br>
         The sound driver is ALSA, PulseAudio is not supported.
         USB DACs are automatically recognized when connected and are listed in the MPD settings in step 4,
         but DAC HATs that are connected to I2S using the GPIO port of the RasberryPi are not automatically recognized and need to be registered.
         Once registered, the sound device can be sound checked using the "speaker-test" command.
         <br>
         </p>

         <br>
         <h3>Step 3 : Source Volume</h3>
         <p class="bodytext2">
         Did you get any sound with Sound Check?
         <br>
         Next, use this form to register the NAS where your music library is stored.
         When the NAS is mounted successfully, [ mute ] will automatically create a symbolic link to the /music directory in MPD.
         If not, please check your SMB version. In most cases "vers=1.0" should work.
         <br>
         </p>

         <br>
         <h3>Step 4 : MPD</h3>
         <p class="bodytext2">
         Now it's time to set up MPD.
         After successful installation, you will be able to configure various settings.
         In particular, the ability to change the Decoder Plugin settings directly is an unique feature not found in other distributions.
         <br>
         </p>

         <br>
         <h3>Step 5 : Web Radio List</h3>
         <p class="bodytext2">
         Web Radio Streaming playlists can be registered on [ mute ].
         The destination of the list will be music directory (.../music/Web_Radio), so you can browse and play it with your client application.
         <br>
         A link to <a href="https://jcorporation.github.io/webradiodb/" target="_blank">[ webradiodb ]</a>, a database of web radio stations, is also provided.
         <br>
         </p>

         <br>
         <h3>Step 6 : Other Settings</h3>
         <p class="bodytext2">
         In this step,you can configure the following steps:
         <br> 1. Last.fm scribble settings
         <br> 2. Generate Coverart by getcover - get cover art image from music files ; FLAC, ALAC, and AAC
         <br> 3. Copy buttons for the host and server names for use with client apps such as yaMPC ( very useful to use on iPad )
         <br> 4. Dark Mode Switch
         <br> 5. System Startup Sound Switch
         <br>
         </p>

         <br>
         <div class="separator"><hr></div>

         <h2>License</h2>
         <p class="bodytext2">
         <br>
         [ mute ] ©2025 Yoichi KITAMURA / <a href="https://kitamura-design.format.com" target="_blank">kitamura_design</a>
         <br>
         <br>
         Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
         to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
         and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
         <br>
         <br>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
         <br>
         <br>
         THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
         INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
         IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
         TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
         <br>
         <br>
         </p>

         <div class="separator"><hr></div>
HTML

cat <<HTML
         <h2>Dependencies</h2>
         <p class="bodytext2">
	 <br>
         This WebApp is written by BASH for the RasberryPi OS and consists of various shell script CGIs, which are accessed and operated by a web browser via LAN.
         The following languages, middleware, packages, and libraries are required for operation.
         <br>
         </p>
HTML

BASH_INFO1=$(bash --version | sed -n 1p | cut -d "(" -f 1)
BASH_INFO2=$(bash --version | sed -n 2p)

cat <<HTML
         <br>
         <h3><a href="https://tiswww.case.edu/php/chet/bash/bashtop.html" target="_blank">bash - GNU Bourne-Again SHell</a></h3>
         <p class="bodytext2">
         ${BASH_INFO1}
         <br>
	 ${BASH_INFO2}
	 <br>
         </p>
HTML

LIGHTTPD_INFO=$(lighttpd -v | cut -d "(" -f 1)

cat <<HTML
         <br>
         <h3><a href="https://redmine.lighttpd.net/projects/lighttpd/wiki/" target="_blank">lighttpd - a fast, secure and flexible web server</a></h3>
         <p class="bodytext2">
	 ${LIGHTTPD_INFO}<br>
         Jan Kneschke [jan@kneschke.de]
         <br>
         </p>
HTML

MPD_INFO1=$(cat /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt | sed -n 1p | cut -d "(" -f 1)
MPD_INFO2=$(cat /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt | sed -n 2p | cut -d "<" -f 1)
MPD_INFO3=$(cat /var/www/cgi-bin/MPD/MPD_conf/temp/mpd_v.txt | sed -n 3p | cut -d "<" -f 1)

cat <<HTML
         <br>
         <h3><a href="http://www.musicpd.org/" target="_blank">MPD - A daemon for playing music</a></h3>
         <p class="bodytext2">
	 ${MPD_INFO1}<br>
	 ${MPD_INFO2}<br>
	 ${MPD_INFO3}<br>
         Max Kellermann [max.kellermann@gmail.com]
         <br>
         </p>
HTML

MPC_INFO=$(mpc help | sed -n 2p)

MPDSCRIBBLE_INFO1=$(mpdscribble -V | sed -n 1p)
MPDSCRIBBLE_INFO3=$(mpdscribble -V | sed -n 3p | cut -d "<" -f 1)
MPDSCRIBBLE_INFO4=$(mpdscribble -V | sed -n 4p | cut -d "<" -f 1)

cat <<HTML
         <br>
         <h3><a href="https://www.musicpd.org/clients/mpc/" target="blank">mpc - a command-line client for the Music Player Daemon (MPD)</a></h3>
         <p class="bodytext2">
	 ${MPC_INFO}<br>
         Max Kellermann [max.kellermann@gmail.com]
         <br>
         </p>

         <br>
         <h3><a href="https://www.musicpd.org/clients/mpdscribble/" target="_blank">mpdscribble - A Music Player Daemon (MPD) client which submits information about tracks being played to a scrobbler (e.g. last.fm).</a></h3>
         <p class="bodytext2">
	 ${MPDSCRIBBLE_INFO1}<br>
         ${MPDSCRIBBLE_INFO3}<br>
         ${MPDSCRIBBLE_INFO4}<br>
         Max Kellermann [max.kellermann@gmail.com]
         <br>
         </p>
HTML

NKF_INFO1=$(nkf -v | sed -n 1p | cut -d "(" -f 1)
NKF_INFO2=$(nkf -v | sed -n 2p)
NKF_INFO3=$(nkf -v | sed -n 3p)

cat <<HTML
         <br>
         <h3><a href="https://github.com/nurse/nkf?tab=readme-ov-file#name" target="_blank">nkf - Network Kanji Filter</a></h3>
         <p class="bodytext2">
         ${NKF_INFO1}<br>
	 ${NKF_INFO2}<br>
         ${NKF_INFO3}<br>
         </p>
HTML

LSOF_VER=$(apt list lsof | cut -d " " -f 2 | sed -n 2p | cut -d "+" -f1)

cat <<HTML
         <br>
         <h3>lsof - list open files</h3>
         <p class="bodytext2">
	 lsof ${LSOF_VER}<br>
         Written by Victor A.Abell [abe@purdue.edu] of Purdue University.
         <br>
         </p>
HTML

BC_INFO1=$(bc -v | sed -n 1p)
BC_INFO2=$(bc -v | sed -n 2p)

cat <<HTML
         <br>
         <h3>bc - An arbitrary precision calculator language</h3>
         <p class="bodytext2">
	 ${BC_INFO1}<br>
         ${BC_INFO2}<br>
         Philip A. Nelson [philnelson@acm.org].
         <br>
         </p>
HTML

PMOUNT_VER=$(echo pmount $(sudo pmount -V))

cat <<HTML
         <br>
         <h3>pmount - mount arbitrary hotpluggable devices as normal user</h3>
         <p class="bodytext2">
	 ${PMOUNT_VER}<br>
         Developed by Martin Pitt [martin.pitt@canonical.com]
         <br>
         Maintained by Vincent Fourmond [fourmond@debian.org]
         <br>
         </p>

         <br>
         <h3><a href="https://www.openaudiolab.com/yampc/getcover/jp/" target="_blank">getcover - get cover art image from music files</a></h3>
         <p class="bodytext2">
         Yasuyuki Suzuki [contact.yampc@gmail.com]
         <br>
         <a href="https://www.openaudiolab.com">www.openaudiolab.com</a>
         </p>

         <br>
         <h3><a href="https://clipboardjs.com" target="_blank">clipboard.js</a></h3>
         <p class="bodytext2">
         Modern copy to clipboard. No Flash. Just 3kb gzipped.
         <br>
         ©Zeno Rocha
         <br>
         </p>

        <br>
         <h3><a href="https://fonts.google.com/specimen/Palanquin/about" target="_blank">Palanquin</a></h3>
         <p class="bodytext2">
         Palanquin is a Unicode-compliant Latin and Devanagari text type family designed for the digital age. 
         The Devanagari is monolinear and was designed alongside the sans serif Latin.
         <br>
         Designed by Pria Ravichandran
         <br>
         </p>
         
         <div class="separator"><hr></div>

  </body>
</html>
HTML
