# boot.py

import esp
import gc
import network
import time
import framebuf
from umqtt.simple import MQTTClient
from display import Display
from logoboot import ctrlzzz0, ctrlzzz1, ctrlzzz2, ctrlzzz3, ctrlzzz4
import stato

esp.osdebug(None)
gc.collect()

# Le credenziali Wi-Fi e l'indirizzo del broker MQTT stanno in config.py,
# che non viene caricato su GitHub. Copia config.example.py in config.py
# e compila i valori.
from config import WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER

MQTT_CLIENT_ID = b'ctrl_zzz'

# === Inizializzazione display e logo ===
display = Display()

# Converte i frame bytearray in oggetti FrameBuffer una sola volta
frames = [
    framebuf.FrameBuffer(ctrlzzz0, 128, 64, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(ctrlzzz1, 128, 64, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(ctrlzzz2, 128, 64, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(ctrlzzz3, 128, 64, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(ctrlzzz4, 128, 64, framebuf.MONO_HLSB),
]

def mostra_logo(loop=1):
    for _ in range(loop):
        for frame in frames:
            display.mostra_logo(frame)
            time.sleep(0.3)


# === Connessione Wi-Fi ===
def connect_wifi():
    print("Connessione al Wi-Fi", end="")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    time.sleep(1)
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)
    
    tentativi = 0
    while not wifi.isconnected() and tentativi < 100:
        mostra_logo()  # Mostra animazione durante la connessione
        print(".", end="")
        tentativi += 1

    if wifi.isconnected():
        print(" Connesso!")
        print("IP:", wifi.ifconfig()[0])
    else:
        print("Timeout Wi-Fi")
    return wifi

# === Connessione MQTT ===
def connect_mqtt():
    print("Connessione al broker MQTT", end="")
    tentativi = 0
    client = None

    while tentativi < 30:
        try:
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
            client.connect()
            print(" Connesso!")
            display.display_centrato("MQTT OK", 50)
            display.display.show()
            time.sleep(1)
            return client
        except Exception as e:
            mostra_logo()  # Animazione anche durante tentativi MQTT
            print(".", end="")
            tentativi += 1

    print("\n❌ Timeout MQTT")
    display.display_centrato("MQTT FAIL", 50)
    display.display.show()
    time.sleep(1)
    return None

    
def ricollega_mqtt():
    global mqtt_client
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
        client.connect()
        mqtt_client = client
        print("🔁 Riconnesso a MQTT!")
        display.testo_centrato("MQTT OK", 50)
    except Exception as e:
        print("❌ Fallita riconnessione MQTT:", e)
        mqtt_client = None

# === Esecuzione iniziale ===
stato.wifi = connect_wifi()
mostra_logo(loop=2)
stato.mqtt_client = connect_mqtt()
time.sleep(1)



