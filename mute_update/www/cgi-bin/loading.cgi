#!/bin/bash

# loading.cgi : Call Tab menu                      #
# (C)2022 kitamura_design <kitamura_design@me.com> #

query=$(date +%Y%m%d%I%M%S)

cat << HTML
Content-type: text/html; charset=utf-8

<!DOCUTYPE html>
<html>

  <head>
     <link rel="stylesheet" type="text/css" href="/css/main.css?$query">
     <meta http-equiv="refresh" content="0; ${QUERY_STRING}">
  </head>

  <body>
   <div id="loading-top2">
     <div class="loader">
        <div class="loadingtext">Loading ...</div>
        <progress class="loading"></progress>
     </div>
   </div>
  </body>

</html>
HTML
