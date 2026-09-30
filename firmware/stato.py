# stato.py
mqtt_client = None
wifi = None

def wifi_connessa():
    return wifi.isconnected() if wifi else False
