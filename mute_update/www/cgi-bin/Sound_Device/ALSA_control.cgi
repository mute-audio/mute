#!/bin/bash

# ALSA_control.cgi
# (C)2026 kitamura_design <kitamura_design@me.com> #
# Collaborated with Gemini

# Persing from QUERY_STRING
card=$(echo "$QUERY_STRING" | sed -n 's/.*card=\([0-9]*\).*/\1/p')
numid=$(echo "$QUERY_STRING" | sed -n 's/.*numid=\([0-9]*\).*/\1/p')
val=$(echo "$QUERY_STRING" | sed -n 's/.*val=\([0-9]*\).*/\1/p')

# Exec amixer to switch DSP filter
if [ -n "$card" ] && [ -n "$numid" ] && [ -n "$val" ]; then
    sudo amixer -c "$card" cset numid="$numid" "$val" > /dev/null 2>&1
fi

echo "Content-type: text/plain"
echo ""
echo "OK"
