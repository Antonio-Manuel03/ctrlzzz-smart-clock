from machine import Pin
from time import sleep
#import melodie

class Ventola:
    def __init__(self,pin,pin_led_blu,pin_led_rosso,allarme,soglia_alta=26,soglia_bassa=18):

        self.ventola = Pin(pin, Pin.OUT)
        self.led_blu = Pin(pin_led_blu, Pin.OUT)
        self.led_rosso = Pin(pin_led_rosso, Pin.OUT)

        self.soglia_alta = soglia_alta  # attiva raffreddamento
        self.soglia_bassa = soglia_bassa  # accende LED rosso (opzionale)
        self.attivo = False


    def get_ventola_attiva(self):
        return self.attivo

    def set_soglia_alta(self,soglia_alta):
        self.soglia_alta = soglia_alta

    def set_soglia_bassa(self,soglia_bassa):
        self.soglia_bassa = soglia_bassa

    def accendi(self):
        self.ventola.on()
        self.attivo = True
        #self.allarme.play(melodia_utenze_on,150,512)
        print("Ventola accesa")

    def spegni(self):
        self.ventola.off()
        self.attivo = False
        #self.allarme.play(melodia_utenze_off,150,512)
        print("Ventola spenta")

    def aggiorna(self, temperatura):
        if temperatura is None:
            return  # errore lettura

        if temperatura > self.soglia_alta:  #aria fredda
            print("accendo aria fredda")
            self.accendi()
            self.led_blu.on()
            self.led_rosso.off()

        elif temperatura < self.soglia_bassa:   #aria calda
            print("accendo aria calda")
            self.accendi()
            self.led_blu.off()
            self.led_rosso.on()
        else:
            print("ventola spenta")
            self.spegni()
            self.led_blu.off()
            self.led_rosso.off()
