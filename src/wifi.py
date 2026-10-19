import network
import urequests
import json
import time
from machine import Timer

settings = {"isLoaded": False}
timerWifiShutoff = Timer()

# A hung request must not freeze the main loop (and with it the button)
REQUEST_TIMEOUT_S = 8

# Called while waiting for wifi so the caller can keep polling the button
idle_hook = None

def set_idle_hook(fn):
    global idle_hook
    idle_hook = fn

# Load settings from the settings.json file
try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    settings["isLoaded"] = True
    print("Loaded settings.json successfully")
except OSError:
    print("Could not find settings.json file")


def disconnect_wifi():
    print("Disconnecting from WiFi...")
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        wlan.active(False)
        print("Disconnected from WiFi")
    else:
        print("No active WiFi connection to disconnect")

def log_visible_networks(wlan):
    # Only called after a failed join so a successful join is not slowed by the ~0.7s scan
    print(f"WiFi status code: {wlan.status()}")
    try:
        for ssid, _, channel, rssi, _, _ in sorted(wlan.scan(), key=lambda n: -n[3]):
            print(f"  seen: {ssid.decode()} ch {channel} rssi {rssi}")
    except Exception as e:
        print(f"WiFi scan failed: {e}")

def connect_wifi():
    try:
        print("Connecting to WiFi...")
        if not settings["isLoaded"]:
            print("settings.json not loaded, cannot connect to WiFi")
            return

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        # The first join often fails on a weak signal, so try twice
        for attempt in range(2):
            if wlan.isconnected():
                break
            print(f"Connecting to WiFi: {settings['wifi_ssid']}")
            wlan.connect(settings['wifi_ssid'], settings['wifi_password'])
            # Wait for connection with timeout
            max_wait = 20
            while max_wait > 0:
                if wlan.isconnected():
                    break
                max_wait -= 1
                print("Waiting for connection...")
                for _ in range(20):
                    if idle_hook:
                        idle_hook()
                    time.sleep_ms(50)
            
            if wlan.isconnected():
                print("Connected to WiFi")
                print(wlan.ifconfig())
                print(f"WiFi signal: {wlan.status('rssi')} dBm")

                timerWifiShutoff.init(period=(120000), mode=Timer.ONE_SHOT, callback=lambda t: disconnect_wifi())
            else:
                print("Failed to connect to WiFi")
                log_visible_networks(wlan)

        is_connected = wlan.isconnected()
        print(f"WiFi connected: {is_connected}")
        return is_connected
    except Exception as e:
        print(f"Error connecting to WiFi: {e}")
        return False

def reportPaActivation():
    try:
        if not connect_wifi():
            print("Not connected to WiFi, cannot report PA activation")
            return False
        print("Reporting PA activation to Adafruit IO")
        #https://io.adafruit.com/api/v2/jongarrison/feeds/ptmsc-hydrophone-listens
        username = settings["adafruit_username"]
        feed = settings["adafruit_feed"]
        key = settings["adafruit_key"]
  
  
        # Get current value
        total_listens = 1

        try:
            get_url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed}/data/last"
            headers = {'X-AIO-Key': key}
            response = urequests.get(get_url, headers=headers, timeout=REQUEST_TIMEOUT_S)
            
            if response.status_code == 200:
                data = json.loads(response.text)
                print(f"Current data: {data}")
                total_listens = int(float(data['value']))
                total_listens = total_listens + 1
                
            response.close()
        except Exception as e:  
            print(f"Error getting current value: {e}")
            #this is not critical so just set to 1
            total_listens = 1

        print(f"Reporting to {username} feed {feed} with key {key}")
        url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed}/data"
        headers = {'X-AIO-Key': key, 'Content-Type': 'application/json'}
        data = {'value': total_listens}  # Increment by 1
        response = urequests.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT_S)
        ok = response.status_code == 200
        if ok:
            print("PA activation reported successfully")
        else:
            print(f"Failed to report PA activation: {response.status_code} {response.text}")
        response.close()
        return ok
    except Exception as e:
        print(f"Error reporting PA activation: {e}")
        return False


def reportDeviceHeartbeat():
    try:
        if not connect_wifi():
            print("Not connected to WiFi, cannot report device heartbeat")
            return False
        print("Reporting device heartbeat to Adafruit IO")
        #https://io.adafruit.com/api/v2/jongarrison/feeds/ptmsc.ptmsc-hydrophone-heartbeat
        username = settings["adafruit_username"]
        feed = settings["adafruit_heartbeat_feed"]
        key = settings["adafruit_key"]

        print(f"Reporting to {username} feed {feed} with key {key}")
        url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed}/data"
        headers = {'X-AIO-Key': key, 'Content-Type': 'application/json'}
        data = {'value': 1}  # value is required, but not important for heartbeat
        response = urequests.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT_S)
        ok = response.status_code == 200
        if ok:
            print("heartbeat reported successfully")
        else:
            print(f"Failed to report heartbeat: {response.status_code} {response.text}")
        response.close()
        return ok
    except Exception as e:
        print(f"Error reporting heartbeat: {e}")
        return False