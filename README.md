# PTMSC Hydrophone Button with Wifi Based Use Reporting

Basic pico2W based micropython device. Consisting of:

 * A momentarily closed button on pin 18. Closing the button connects with ground.
 * An LED (with current limiting resistor) on pin 16
 * A relay that is high triggered on pin 15

Currently, the public report of hydrophone speaker button pushes can be found here:
https://io.adafruit.com/jongarrison/feeds/ptmsc-hydrophone-listens

# Setup

This project needs a src/secrets.json which looks like this:

    {
        "wifi_ssid": "your-wifi-ssid",
        "wifi_password": "your-wifi-password",
        "adafruit_username": "your-adafruitio-username",
        "adafruit_key": "your-adafruitio-key",
        "adafruit_feed": "your-adafruitio-feed",
        "adafruit_heartbeat_feed": "your-adafruitio-heartbeat-feed"
    }

## Micropython loading

Code can be loaded with Thonny or mpremote. See notes for some of my mpremote resources.

