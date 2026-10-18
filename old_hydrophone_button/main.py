# Code to exercise the PTMSC Audio Control Board
# this setup has:
#	a momentary switch, normally open, shorts to ground when pushed
#	An LED, part of the switch
#	A solid state AC relay.  Conducts when control input is above 3V

# This code exercises the basics
from machine import Pin
from time import ticks_ms, ticks_diff

# for simplicity, just use a loop counter instead of checking time
LOOPLIM = 10000
OnTimeSecsLimit = 2*60*1000	

# my demo board has these three connections
sw=Pin(11, Pin.IN, Pin.PULL_UP)		# switch shorts this pin to ground when pressed,  reads 1 when not pushed
led=Pin(15, Pin.OUT)		# LED is on when this pin is high
pwr=Pin(16, Pin.OUT)		# relay is on when this pin is high

pwr.off()
led.off()

startTime = 0
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
            startTime = ticks_ms()
        elif loops > LOOPLIM:	# latch loop count to just beyond limit
            loops = LOOPLIM + 1
    else:				#Switch is off
        loops = 0
        
    if pwr.value() == 1:	#if power is on
        if ticks_diff(ticks_ms(), startTime) > OnTimeSecsLimit:
            led.toggle()
            pwr.toggle()