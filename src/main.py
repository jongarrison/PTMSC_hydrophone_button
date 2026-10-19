from machine import Pin, Timer
import time
from adafruit_mpy_debouncer import Button
from wifi import settings, set_idle_hook, reportPaActivation, reportDeviceHeartbeat

# How long the relay (and button LED) stay on after a press, in seconds
PA_ON_SECONDS = settings.get("pa_on_seconds", 10)

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

led=Pin(15, Pin.OUT, value=0)
sw=Pin(11, Pin.IN, Pin.PULL_UP)	#20	# the switch shorts GP18 to ground when pressed
pwr=Pin(16, Pin.OUT, value=0)

switch = Button(sw)

def disablePaSystemNormal():
    print("Disabling PA system")
    led.off()
    pwr.off()

def enablePaSystemNormal():
    print("Enabling PA system")
    led.on()
    pwr.on()

    timerPaShutoff.init(period=PA_ON_SECONDS * 1000, mode=Timer.ONE_SHOT, callback=lambda t: disablePaSystemNormal())

# Network reports are queued and run from the main loop, so a network problem can never stop the button
RETRY_DELAYS_S = (5, 30, 120)  # wait before each retry of a failed report, then give up
reportQueue = []  # entries: [report function, retries used, ticks_ms when due]

def queueReport(fn):
    reportQueue.append([fn, 0, time.ticks_ms()])

def runDueReport():
    now = time.ticks_ms()
    for entry in reportQueue:
        if time.ticks_diff(now, entry[2]) >= 0:
            break
    else:
        return
    fn, retries, _ = entry
    try:
        ok = fn()
    except Exception as e:
        print(f"Report error: {e}")
        ok = False
    if ok:
        reportQueue.remove(entry)
    elif retries < len(RETRY_DELAYS_S):
        print(f"Report failed, retrying in {RETRY_DELAYS_S[retries]}s")
        entry[1] = retries + 1
        entry[2] = time.ticks_add(time.ticks_ms(), RETRY_DELAYS_S[retries] * 1000)
    else:
        print("Report failed, giving up")
        reportQueue.remove(entry)

def pollButton():
    switch.update()
    if switch.short_count == 1:
        print("Short Press Activate!")
        enablePaSystemNormal()
        queueReport(reportPaActivation)

# wifi.py calls this while waiting to connect, so a press still switches the relay
set_idle_hook(pollButton)

dailyHeartbeatMs = 24 * 60 * 60 * 1000 # 24 hours
#dailyHeartbeatMs = 10 * 1000 # 10 seconds #debug

queueReport(reportDeviceHeartbeat)  # report when the system starts
timerHeartbeat.init(period=dailyHeartbeatMs, mode=Timer.PERIODIC, callback=lambda t: queueReport(reportDeviceHeartbeat))

print("basic setup complete")

# Main loop
while True:
    pollButton()
    runDueReport()