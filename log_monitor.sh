#!/bin/bash
# Show the Pico's log output. Ctrl-D restarts the program, Ctrl-] exits.
cd "$(dirname "$0")"
exec .venv/bin/mpremote repl
