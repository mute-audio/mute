#!/bin/bash

# sync_AirPlay_volume.sh                           #
# Sync shairport-sync volume settings with MPD ALSA output
# (C)2026 kitamura_design <kitamura_design@me.com> #

MPD_CONF="${MPD_CONF:-/etc/mpd.conf}"
SPS_CONF="${SPS_CONF:-/etc/shairport-sync.conf}"

# Get value from #ALSA audio_output block in mpd.conf (ignore commented lines)
get_mpd_alsa() {
  sed -n '/^#ALSA$/,/^}/p' "$MPD_CONF" \
    | grep -E "^[[:space:]]+$1[[:space:]]" \
    | head -n 1 | cut -d '"' -f 2
}

MIXER_TYPE=$(get_mpd_alsa mixer_type)
DEVICE=$(get_mpd_alsa device)
MIXER_CTL=$(get_mpd_alsa mixer_control)

# Fallback
[ -z "$DEVICE" ] && DEVICE="default"
case "$MIXER_CTL" in *"Not Assigned"*) MIXER_CTL="" ;; esac

# Mixer device for shairport : "hw:1,0" -> "hw:1"
MIXER_DEV="${DEVICE%%,*}"

# Volume settings
case "$MIXER_TYPE" in
  none)
    IGNORE_VOL="yes"
    MIXER_LINES=""
    ;;
  hardware)
    IGNORE_VOL="no"
    if [ -n "$MIXER_CTL" ]; then
      MIXER_LINES="    mixer_control_name = \"${MIXER_CTL}\";
    mixer_device = \"${MIXER_DEV}\";"
    else
      MIXER_LINES=""          # Not Assigned -> software attenuation
    fi
    ;;
  *)                          # software / unknown
    IGNORE_VOL="no"
    MIXER_LINES=""
    ;;
esac

BEFORE=$(md5sum "$SPS_CONF" | cut -d ' ' -f 1)

# 1. general : ignore_volume_control
sudo sed -i -E "s|^([[:space:]]*)ignore_volume_control[[:space:]]*=.*$|\1ignore_volume_control = \"${IGNORE_VOL}\";|" "$SPS_CONF"

# 2. alsa : rewrite whole block
TMP=$(mktemp)
sed '/^alsa = {$/,/^};$/d' "$SPS_CONF" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' > "$TMP"
{
  echo ""
  echo "alsa = {"
  echo "    output_device = \"${DEVICE}\";"
  [ -n "$MIXER_LINES" ] && echo "$MIXER_LINES"
  echo "};"
} >> "$TMP"
sudo cp "$TMP" "$SPS_CONF"
rm -f "$TMP"

AFTER=$(md5sum "$SPS_CONF" | cut -d ' ' -f 1)

# Restart only when changed & enabled
if [ "$BEFORE" != "$AFTER" ] && sudo systemctl is-enabled --quiet shairport-sync 2>/dev/null; then
  sudo systemctl restart shairport-sync
fi

exit 0
