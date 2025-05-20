from machine import Pin, Timer
import time
from adafruit_mpy_debouncer import Button
from wifi import connect_wifi, disconnect_wifi, reportPaActivation, reportDeviceHeartbeat

print("starting basic setup - V0.1")
timerPaShutoff = Timer()
timerHeartbeat = Timer()

# Pin	Desig	Use	Comments
# 21	GP16	SSR high side control (+)	
# 23	GND	    SSR low side control (-)	
# 15	GP11	PB Switch input	Configure as Pin.PULL_UP
# 13	GND	    PB Swith low side	Switch joins GP11 to GND when pushed
# 20	GP15	PB Switch LED drive	May want to define this as a PWM output to allow for fading
# 18	GND	    PB Switch LED low side
# see also: https://datasheets.raspberrypi.com/picow/pico-2-w-pinout.pdf

led=Pin(15, Pin.OUT) #16
sw=Pin(11, Pin.IN, Pin.PULL_UP)	#20	# the switch shorts GP18 to ground when pressed
pwr=Pin(16, Pin.OUT) #15

switch = Button(sw)
connect_wifi()

dailyHeartbeatMs = 24 * 60 * 60 * 1000 # 24 hours
#dailyHeartbeatMs = 10 * 1000 # 10 seconds #debug

reportDeviceHeartbeat() #report when the system starts
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