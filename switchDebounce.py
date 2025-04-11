# Simple routine to monitor a momentary pushbutton input and toggle an output when the button is pushed
from machine import Pin

# for simplicity, just use a loop counter instead of checking time
LOOPLIM = 20000

# my demo board has these three connections
led=Pin(16, Pin.OUT)
sw=Pin(18,Pin.IN, Pin.PULL_UP)		# the switch shorts GP18 to ground when pressed
pwr=Pin(15, Pin.OUT)

pwr.off()
led.off()

loops = 0

# this piece of cruft just makes sure the switch stays in the connected state for enough time to
# debounce.  Otherwise, we might quickly cycle through a bunch of on/off states.
# really, we should just require the switch to stay closed for 100 mSec.
while True:
    if sw() == 0:		#Switch is pressed
        loops += 1
        if loops == LOOPLIM:  # if we hit limit, turn on power   
            led.toggle()
            pwr.toggle()
            loops = 0
        elif loops > LOOPLIM:	# latch loop count to just beyond limit
            loops = LOOPLIM + 1
    else:				#Switch is off
        loops = 0