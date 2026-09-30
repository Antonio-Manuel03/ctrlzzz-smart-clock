from machine import Pin
import dht


class SensoreTemperatura:
    def __init__(self, pin):
        self.sensore = dht.DHT22(Pin(pin))

    def leggi(self):
        try:
            self.sensore.measure()
            temp = self.sensore.temperature()  # restituisce °C
            print("Temperatura:", temp, "°C")
            return temp
        except Exception as e:
            print("Errore lettura temperatura:", e)
            return None
