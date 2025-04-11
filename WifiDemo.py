# Socket Demo  Open a UDP socket server on the local WiFi and accept messages there.
# This code runs in conjunction with an Android app built in MIT App Inventor.  The app has four pairs of buttons
# Basically, they are on/off buttons that send a string with three character ID and a 1 or zero for the desired state.
from machine import Pin     # for pin based I/O
from machine import Timer   # for an interrupt based timer routine
from time import sleep
import network
import socket


DEBUG = True        # used to switch between two networks
myPort = 5247       # arbitrary but stay above 4096

# my demo board has 5 LEDs of differing colors
red = Pin(10,Pin.OUT)   # Just an LED
grn = Pin(11,Pin.OUT)   # Just an LED
blu = Pin(12,Pin.OUT)   # Just an LED
yel = Pin(13,Pin.OUT)   # WiFi connection indication, then command reception
wht = Pin(14,Pin.OUT)   # Power - just flashes at 1Hz when the program is up and running

red.on()        # init all the lights on
grn.on()
blu.on()
yel.on()
wht.on()

# the demo board also is connected to an SPST electromechanical relay that happens to be connected to a 12V fan
rly = Pin(17,Pin.OUT)
rly.off()       # init the fan off

lastLEDState=1    # the LED is on

# Timer callback to toggle the white LED, theoretically indicates that the Pico code is still working
def workingCB(timer):
    global lastLEDState
    
    if lastLEDState == 0:
        wht.on()
        lastLEDState = 1
    else:
        wht.off()
        lastLEDState = 0

# create a timer to keep firing workingCB
workTimer = Timer(period=1000, mode=Timer.PERIODIC, callback=workingCB)

# routines to flash the yellow LED to indicate a command received via the network
def flashCommsLED():
    yel.on()
    # set a timer to turn off the LED after a brief time
    commsTimer = Timer(period=100, mode=Timer.ONE_SHOT, callback=commsLEDCB)
    
def commsLEDCB(timer):
    yel.off()


# method to provide connection to WiFi
def connect():
    if not DEBUG:
        ssid = 'YourWifi'
        password = 'yourpassword'
    else:     
        ssid = 'TestWiFi'
        password = 'YourTestPassword'
        
    # Connect to a WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while not wlan.isconnected():
        print('Connecting…')
        wlan.connect(ssid, password)
        waittime = 0
        while not wlan.isconnected():
            sleep(0.1)
            waittime += 1
            if waittime > 65:
                print('Unable to connect to WLAN ' + ssid)
                waittime = 0
    ip = wlan.ifconfig()[0]
    return ip

#Create a UDP Socket to receive commands
def open_socket(ip):
    address = (ip, 5247)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.setblocking(True)
    return sock

# connect to WiFi
myIP=connect()
print(f'connected to WiFi as {myIP}')
print(f'Listening on port {myPort}')

#create a socket for UDP requests
serverSock = open_socket(myIP)
print(serverSock)
yel.off()       # this action indicates a successful connection to the WLAN

# listen for messages, control the LEDs or relay:w

while True:
    try:
        data,address = serverSock.recvfrom(128)
        msgtxt = data.decode()
        print(f"Received message: {msgtxt} from {address}")
        
        if len(msgtxt) == 5:
            if msgtxt[:3] == "red":
                if msgtxt[4] == '1':
                    red.on()
                else:
                    red.off()
            elif msgtxt[:3] == "grn":
                if msgtxt[4] == '1':
                    grn.on()
                else:
                    grn.off()
            elif msgtxt[:3] == "blu":
                if msgtxt[4] == '1':
                    blu.on()
                else:
                    blu.off()
            elif msgtxt[:3] == "rly":
                if msgtxt[4] == '1':
                    rly.on()
                else:
                    rly.off()
    
        flashCommsLED() # indicate we received a message
    
    except OSError as err_msg:
        print(f"Error occurred: {err_msg}")