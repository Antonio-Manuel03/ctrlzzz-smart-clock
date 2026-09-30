from machine import Pin, I2C
from tsl2561 import TSL2561


class Luce:
    def __init__(self, pin_luce, SCL=18, SDA=19, soglia=39):
        self.i2c = I2C(1, scl=Pin(SCL), sda=Pin(SDA))
        self.sensore = TSL2561(self.i2c) #driver
        self.luce = Pin(pin_luce, Pin.OUT)
        self.soglia = soglia
        self.lux_max = 10
    
    def get_luminosita(self):
        return self.normalizza_lux(self.sensore.read_lux())
    
    def get_lux(self):
        return self.sensore.read_lux()
    
    def set_soglia(self,soglia):
        self.soglia=soglia
    
    def set_lux_max(self,lux_max):
        self.lux_max = lux_max
    
    def normalizza_lux(self, lux): #cambiare lux max per avere scala più sensibile
        percentuale = int((lux / self.lux_max) * 100)
        percentuale = max(0, min(100, percentuale))  # clamp
        return percentuale
    
    def aggiorna(self, modalita):
        try:
            lux = self.normalizza_lux(self.sensore.read_lux()) #sensore di luminosità
            print("Luminosità:", lux,)

            if modalita == "notte":
                self.luce.off()
            else:
                if lux < self.soglia:
                    self.luce.on()
                    print("Luce accesa")
                else:
                    self.luce.off()
                    print("Luce spenta")
        except Exception as e:
            print("Errore sensore luce:", e)

