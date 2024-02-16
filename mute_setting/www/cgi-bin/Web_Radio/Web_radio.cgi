#!/bin/bash

# Web_radio.cgi                                 #
# (C)2024 kitamura_design <kitamura_design@me.com> #

destDIR="/var/lib/mpd/music/Web_Radio"

cat <<HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>
       <head>
        <link rel="stylesheet" type="text/css" href="/css/main.css?$query">
        <script>

          function keepHover(){
              target = parent.document.getElementById("WebRadio");
              if (target != null){
                  target.className = "menutab-keephover";
              }
            }

          function offHover(){
              target = parent.document.getElementById("WebRadio");
              if (target != null){
                  target.className = "menutab";
                  }
            }
        </script>
        </head>

        <body id="iframe" onLoad="keepHover()" onunload="offHover()">

        <!-- Title-->
        <h1>Web Radio List</h1>
        <h3>
          <a href="https://jcorporation.github.io/webradiodb/" target="_blank">Check the Radio Stations on "webradiodb"</a>
        </h3>
HTML

####### Streaming (Web Radio) List

	listDIR=$(ls "${destDIR}" 2>/dev/null) #Set PlaylistFile Array

	if [ -z $listDIR ]; then

        cat <<HTML
        <div id="no_list">
        <h3>-- No Web Radio List --</h3>

          <div class="setting-items-wrap">
            <a class="button-disabled">Delete</a>
            <input class="inputbox-single-readonly" value="-- No Station --" readonly>
          </div>

	</div>
HTML
	else

	listM3U="${destDIR}/*m3u"

  for playlistFILE in ${listM3U} ; do

	  playlistNAME=$(echo ${playlistFILE} | cut -d "/" -f 7 | cut -d "." -f 1)

	    cat <<HTML
        <div id="${playlistNAME}">
	      <h3>${playlistNAME}</h3>

HTML
    listNUM=$(cat "${playlistFILE}" | wc -l)

		for ((i=1; i <= $listNUM; i=i+3)); do

		 	j=$(($i + 1))

		 	stationURL=$(sed -n ${j}p "${playlistFILE}")
      stationNAME=$(sed -n ${i}p "${playlistFILE}" | sed -e 's/^#//g')

		 	cat <<HTML
			<div id="$stationNAME" class="setting-items-wrap">
			    <a class="button" href="/cgi-bin/Web_Radio/delete_Web_Radio.cgi?list=${playlistNAME}&name=${stationNAME}">Delete</a>
          <input class="inputbox-single-readonly" value="$stationNAME">
			</div>
HTML
		done

	   cat <<HTML
            </div>
            <div class="separator"><hr></div>
            <br>
HTML
	done
	fi

 #### Web Radio Station Registration Form

        cat <<HTML
        <div id="WebRadio_Form" class="title-btn-title">
          <a href="https://jcorporation.github.io/webradiodb/" target="_blank" class="toggle-on-sw"> Check "webradiodb" </a>
          <h4> Add Station</h4>
        </div>

        <form method=GET action="/cgi-bin/Web_Radio/add_Web_Radio.cgi" onsubmit="" target="_self">
             <ul>
                  <!-- List Title (Playlist File Name) -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="list_title" name="list_title" placeholder="My WebRadio" class="inputbox" required>
                   <label for="">List Title</label>
                </li>

                  <!-- Station Name -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="station_name" name="station_name" placeholder="Station Name" class="inputbox" required>
                   <label for="">Station Name</label>
                </li>

                  <!-- Streaming URL -->
                <li class="setting-items-wrap">
                   <div class="ellipsis-wrap">Aa</div>
                   <input type="text" id="stream_URL" name="stream_URL" placeholder="https://webradio/stream/stream.aac" class="inputbox">
                   <label for="">Stream URL</label>
                </li>
             </ul>
                 <!-- Submit & reset -->
                 <div class="setting-items-wrap">
                   <input id="submit" type="submit" value=" Add " class="button"></input>
                   <input id="reset" type="reset" value=" Reset " class="button2"></input>
                 </div>
        </form>
        </div>

        <div class="separator"><hr></div>

	  </body>
	</html>
HTML

exit 0
