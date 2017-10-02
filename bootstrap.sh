#!/usr/bin/env bash

if [[ "$(id -u)" != "0" ]]; then
    PASS=$(zenity --entry --text="input:")
    CMD=$0
    expect -c "
      set timeout -1
      spawn sudo $CMD
      expect \"assword\" {
        send \"$PASS\n\"
      }
      interact
    "
    exit
fi
sudo bash -c "cat << 'EOF' > ok
$(date +%Y%m%d%H%M%S)
EOF"
echo "complete"

