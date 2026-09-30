from machine import PWM, Pin
from sensore_ir import SensoreIR

class Porta:
    def __init__(self, pin, pinsensore):
        self.pwm = PWM(Pin(pin), freq=50)
        self.aperta = True
        self.angolo_aperto = 180
        self.angolo_chiuso = 110
        self.sensore_ir = SensoreIR(pinsensore)

    def get_porta_aperta(self):
        return self.aperta
    
    def set_angolo_aperto(self, angolo):
        self.angolo_aperto = angolo
        
    def set_angolo_chiuso(self, angolo):
        self.angolo_chiuso = angolo

    def set_angle(self, angle):
        duty_min = 26
        duty_max = 128
        duty = int(duty_min + (angle / 180) * (duty_max - duty_min))
        self.pwm.duty(duty)

    def apri(self):
        self.set_angle(self.angolo_aperto)
        self.aperta = True
        print("apro la porta")

    def chiudi(self):
        self.set_angle(self.angolo_chiuso)
        self.aperta = False
        print("chiudo la porta")

    def aggiorna(self, modalita):
        if modalita == "giorno":
            self.apri()
        elif modalita == "notte":
            if not self.sensore_ir.rileva():
                print("la porta è aperta non posso chuiuderla a chiave")
            else:
                self.chiudi()

