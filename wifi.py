import network
import urequests
import json
from machine import Timer

secrets = {"isLoaded": False}
timerWifiShutoff = Timer()

def disconnect_wifi():
    print("Disconnecting from WiFi...")
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        wlan.active(False)
        print("Disconnected from WiFi")
    else:
        print("No active WiFi connection to disconnect")

def connect_wifi():
    try:
        print("Connecting to WiFi...")
        if not secrets["isLoaded"]:
            print("secrets.json not loaded, cannot connect to WiFi")
            return

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print(f"Connecting to WiFi: {secrets['wifi_ssid']}")
            wlan.connect(secrets['wifi_ssid'], secrets['wifi_password'])
            # Wait for connection with timeout
            max_wait = 20
            while max_wait > 0:
                if wlan.isconnected():
                    break
                max_wait -= 1
                print("Waiting for connection...")
                time.sleep(1)
            
            if wlan.isconnected():
                print("Connected to WiFi")
                print(wlan.ifconfig())

                timerWifiShutoff.init(period=(120000), mode=Timer.ONE_SHOT, callback=lambda t: disconnect_wifi())
            else:
                print("Failed to connect to WiFi")

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
            return
        print("Reporting PA activation to Adafruit IO")
        #https://io.adafruit.com/api/v2/jongarrison/feeds/ptmsc-hydrophone-listens
        username = secrets["adafruit_username"]
        feed = secrets["adafruit_feed"]
        key = secrets["adafruit_key"]
  
  
        # Get current value
        total_listens = 1

        try:
            get_url = f"https://io.adafruit.com/api/v2/{username}/feeds/{feed}/data/last"
            headers = {'X-AIO-Key': key}
            response = urequests.get(get_url, headers=headers)
            
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
        response = urequests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("PA activation reported successfully")
        else:
            print(f"Failed to report PA activation: {response.status_code} {response.text}")
        response.close()
    except Exception as e:
        print(f"Error reporting PA activation: {e}")