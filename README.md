# PTMSC Hydrophone Button with Wifi Based Use Reporting

Basic pico2W based micropython device. Consisting of:

 * A momentarily closed button on pin 18. Closing the button connects with ground.
 * An LED (with current limiting resistor) on pin 16
 * A relay that is high triggered on pin 15

# Setup

This project needs a secrets.json at the root which looks like this:

    {
        "wifi_ssid": "your-wifi-ssid",
        "wifi_password": "your-wifi-password",
        "adafruit_username": "your-adafruitio-username",
        "adafruit_key": "your-adafruitio-key",
        "adafruit_feed": "your-adafruitio-feed"
    }

## Micropython loading

Code can be loaded with Thonny or mpremote. See notes for some of my mpremote resources.
