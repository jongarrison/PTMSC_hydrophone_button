#!/bin/bash
# Copy only settings.json to the Pico, then restart it.
set -e
cd "$(dirname "$0")"
MPREMOTE=.venv/bin/mpremote

$MPREMOTE fs cp src/settings.json :
$MPREMOTE reset
echo "Settings deployed and restarted. Run ./log_monitor.sh to watch the logs."
