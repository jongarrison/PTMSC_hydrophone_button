from machine import Pin, Timer
import time
from adafruit_mpy_debouncer import Button
from wifi import connect_wifi, disconnect_wifi, reportPaActivation, reportDeviceHeartbeat

print("starting basic setup")
timerPaShutoff = Timer()
timerHeartbeat = Timer()

led=Pin(16, Pin.OUT)
sw=Pin(20,Pin.IN, Pin.PULL_UP)		# the switch shorts GP18 to ground when pressed
pwr=Pin(15, Pin.OUT)

switch = Button(sw)
connect_wifi()

dailyHeartbeatMs = 24 * 60 * 60 * 1000 # 24 hours
#dailyHeartbeatMs = 10 * 1000 # 10 seconds #debug
timerHeartbeat.init(period=dailyHeartbeatMs, mode=Timer.PERIODIC, callback=lambda t: reportDeviceHeartbeat())

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


# Main loop
while True:
    switch.update()
    if switch.short_count == 1:
        print("Short Press Activate!")
        enablePaSystemNormal()