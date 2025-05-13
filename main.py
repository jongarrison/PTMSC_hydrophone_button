from machine import Pin
import time
from adafruit_mpy_debouncer import Button

print("starting basic setup")

led=Pin(16, Pin.OUT)
sw=Pin(20,Pin.IN, Pin.PULL_UP)		# the switch shorts GP18 to ground when pressed
pwr=Pin(15, Pin.OUT)

switch = Button(sw)

print("basic setup complete")

def disablePaSystemNormal():
    print("Disabling PA system")
    led.off()
    pwr.off()

def enablePaSystemNormal():
    print("Enabling PA system")
    led.on()
    pwr.on()

    # after 10 seconds, turn off the system
    timerPaShutoff.init(period=10000, mode=Timer.ONE_SHOT, callback=lambda t: disablePaSystemNormal())
    reportPaActivation()


print("starting configuration")

# Load secrets from the secrets.json file
try:
    with open('secrets.json', 'r') as f:
        secrets = json.load(f)
    secrets["isLoaded"] = True
    print("Loaded secrets.json successfully")
except OSError:
    print("Could not find secrets.json file")

print(f"configured secrets: {secrets}")

connect_wifi()

print(f"System configuration complete")

while True:
    switch.update()
    if switch.short_count == 1:
        print("Short Press Activate!")
        enablePaSystemNormal()