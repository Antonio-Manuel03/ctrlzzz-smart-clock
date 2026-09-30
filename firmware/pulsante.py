from machine import Pin
from time import ticks_ms, ticks_diff

class Pulsante:
    def __init__(self, pin, callback_singolo, callback_doppio=None, debounce_ms=200, doppio_click_ms=400):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.callback_singolo = callback_singolo
        self.callback_doppio = callback_doppio
        self.debounce_ms = debounce_ms
        self.doppio_click_ms = doppio_click_ms
        self.ultimo_tocco = 0
        self.secondo_tocco = False
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._pressed)

    def _pressed(self, pin):
        ora = ticks_ms()
        delta = ticks_diff(ora, self.ultimo_tocco)

        if delta < self.debounce_ms:
            return  # Rimbalzo, ignora

        if delta < self.doppio_click_ms and self.secondo_tocco:
            print(f"[{pin}] Doppio tocco!")
            self.secondo_tocco = False
            if self.callback_doppio:
                self.callback_doppio()
        else:
            # Primo tocco, aspetta il secondo
            print(f"[{pin}] Primo tocco (attesa doppio)")
            self.secondo_tocco = True
            self.ultimo_tocco = ora

            # Esegui singolo solo se dopo timeout non arriva il secondo (semplificato: esegue subito)
            if not self.callback_doppio:
                self.callback_singolo()

