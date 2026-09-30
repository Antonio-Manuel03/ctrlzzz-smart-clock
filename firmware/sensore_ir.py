from machine import Pin
import time

class SensoreIR:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN)
        self.presenza = False

    def rileva(self):
        """
        Restituisce True se viene rilevato un ostacolo, False altrimenti.
        """
        stato = self.pin.value()
        self.presenza = (stato == 0)  # HW-S11 manda 0 quando rileva
        return self.presenza

    def stato_testuale(self):
        """
        Restituisce una stringa leggibile dello stato del sensore.
        """
        return "Ostacolo rilevato" if self.presenza else "Nessun ostacolo"
