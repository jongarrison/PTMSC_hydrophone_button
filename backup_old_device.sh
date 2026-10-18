#!/bin/bash
# Copy every file on the connected Pico into old_hydrophone_button/ (a backup of what it is running).
set -e
cd "$(dirname "$0")"
MPREMOTE=.venv/bin/mpremote

mkdir -p old_hydrophone_button
$MPREMOTE fs cp -r : old_hydrophone_button/
echo "Copied Pico files to old_hydrophone_button/"
ls -l old_hydrophone_button
