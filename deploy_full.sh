#!/bin/bash
# Copy all code and settings to the Pico, then restart it.
set -e
cd "$(dirname "$0")"
MPREMOTE=.venv/bin/mpremote

$MPREMOTE fs cp src/main.py src/wifi.py src/adafruit_mpy_debouncer.py src/settings.json :
$MPREMOTE reset
echo "Deployed and restarted. Run ./log_monitor.sh to watch the logs."
