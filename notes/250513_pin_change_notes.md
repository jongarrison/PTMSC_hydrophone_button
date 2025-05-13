Eric's pin mapping:

Pin	Desig	Use	Comments
21	GP16	SSR high side control (+)	
23	GND	SSR low side control (-)	
15	GP11	PB Switch input	Configure as Pin.PULL_UP
13	GND	PB Swith low side	Switch joins GP11 to GND when pushed
20	GP15	PB Switch LED drive	May want to define this as a PWM output to allow for fading
18	GND	PB Switch LED low side

From PicoStuff (https://github.com/bigoleric/PicoStuff/blob/main/switchDebounce.py)

led=Pin(16, Pin.OUT)
sw=Pin(18,Pin.IN, Pin.PULL_UP)		# the switch shorts GP18 to ground when pressed
pwr=Pin(15, Pin.OUT)


"On the Raspberry Pi Pico 2W, pin 18 (GPIO18) is used as part of the SPI interface for the on-board CYW43439 wireless chip. Specifically, GPIO18 serves as the SCK (Serial Clock) line for SPI communication between the RP2350 microcontroller and the wireless module."