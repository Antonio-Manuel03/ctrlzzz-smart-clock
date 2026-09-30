from machine import PWM, Pin
from time import sleep

class Tenda:
    def __init__(self, pin):
        self.servo = PWM(Pin(pin), freq=50)
        self.angolo_aperto = 1
        self.angolo_chiuso = 179

    def set_angle(self, angle):
        duty_min = 40   # corrisponde a 0°
        duty_max = 115  # corrisponde a 180°
        duty = int(duty_min + (angle / 180) * (duty_max - duty_min))
        self.servo.duty(duty)
        sleep(0.5)  # dai tempo al servo di muoversi

    def set_angolo_aperto(self, angolo):
        self.angolo_aperto = angolo

    def set_angolo_chiuso(self, angolo):
        self.angolo_chiuso = angolo

    def apri(self):
        self.set_angle(self.angolo_aperto)
        print("Tenda aperta")

    def chiudi(self):
        self.set_angle(self.angolo_chiuso)
        print("Tenda chiusa")

    def aggiorna(self, modalita):
        if modalita == "giorno":
            self.apri()
        else:
            self.chiudi()

