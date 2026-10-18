# PTMSC Hydrophone Button with Wifi Based Use Reporting

Basic pico2W based micropython device. Consisting of:

 * A momentarily closed button on GP11 (pin 15). Closing the button connects with ground.
 * An LED (with current limiting resistor) on GP15 (pin 20)
 * A relay that is high triggered on GP16 (pin 21)

Currently, the public report of hydrophone speaker button pushes can be found here:
https://io.adafruit.com/jongarrison/feeds/ptmsc-hydrophone-listens

# Settings

All settings live in `src/settings.json`. It also holds passwords and keys, so it is not committed to git. Create it like this:

    {
        "pa_on_seconds": 10,
        "wifi_ssid": "your-wifi-ssid",
        "wifi_password": "your-wifi-password",
        "adafruit_username": "your-adafruitio-username",
        "adafruit_key": "your-adafruitio-key",
        "adafruit_feed": "your-feed-key",
        "adafruit_heartbeat_feed": "your-group-key.your-heartbeat-feed-key"
    }

 * `pa_on_seconds`: how long the relay stays on after a button press (optional, defaults to 10).
 * `wifi_ssid` / `wifi_password`: the wifi network the Pico joins.
 * `adafruit_*`: your Adafruit IO account, key and the feeds that button presses and daily heartbeats are reported to. A feed inside a group is written as `group-key.feed-key`.

After editing, run `./deploy_settings.sh` to send it to the Pico.

# Setup

## Loading code with mpremote

`mpremote` is a command line tool that talks to the Pico over USB. Install it once:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install mpremote

Run the rest from the project root with the Pico plugged in.

Convenience scripts (these wrap the commands below):

 * `./deploy_full.sh` copies all the code and settings to the Pico and restarts it.
 * `./deploy_settings.sh` copies only `src/settings.json` and restarts the Pico.
 * `./log_monitor.sh` shows the Pico's logs.

The individual commands:

Check the Pico is found (look for "MicroPython Board"):

    mpremote connect list

Copy the code to the Pico:

    mpremote fs cp src/main.py src/wifi.py src/adafruit_mpy_debouncer.py src/settings.json :

List the files on the Pico:

    mpremote fs ls :

Watch the logs (anything the code `print`s):

    mpremote repl

In the repl, press Ctrl-D to restart the program and see its startup logs. Press Ctrl-] to exit.

Notes:

 * Only one program can use the USB port at a time, so exit the repl before copying files.
 * `main.py` runs automatically whenever the Pico is powered on.
 * If you have several devices, pick one with `mpremote connect port:/dev/cu.usbmodemXXXX repl`.
 * More notes are in `dev-notes/`.

