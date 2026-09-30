from time import localtime
import _thread


class Sveglia:
    def __init__(self, allarme, display, ora_sveglia=(7, 30), ora_notte=(23, 0), intervallo_acqua=30):
        self.allarme = allarme
        self.display = display
        self.ora_sveglia = ora_sveglia
        self.ora_notte = ora_notte
        self.intervallo_acqua = intervallo_acqua
        self.ora_mqtt = (12, 0)
        self.modalita = "giorno"
        self.ultimo_promemoria_acqua = None
        self.sveglia_suonando = False
        self.sveglia_gestita = False
        self.promemoria_acqua_totali = 0




        print(f"Inizializzato Sveglia con sveglia alle {self.ora_sveglia}, notte alle {self.ora_notte}, intervallo acqua ogni {self.intervallo_acqua} minuti.")

    def get_modalita(self):
        return self.modalita

    def get_ora_corrente(self):
        return self.ora_mqtt
        #offset = 7200  # 2 ore per ora legale, 3600 per solare
        #orario = localtime(time() + offset)
        #return (orario[3], orario[4])
    
    def get_durata_sonno(self):
        notte_min = self._ora_in_minuti(self.ora_notte)
        sveglia_min = self._ora_in_minuti(self.ora_sveglia)
        durata = (sveglia_min - notte_min) % (24 * 60)  # gestisce mezzanotte
        ore = durata // 60
        minuti = durata % 60
        return (ore, minuti)

        
    def set_ora_sveglia_ore(self, ore):
        self.ora_sveglia = (int(ore), self.ora_sveglia[1])

    def set_ora_sveglia_minuti(self, minuti):
        self.ora_sveglia = (self.ora_sveglia[0], int(minuti))

    def set_ora_notte_ore(self, ore):
        self.ora_notte = (int(ore), self.ora_notte[1])

    def set_ora_notte_minuti(self, minuti):
        self.ora_notte = (self.ora_notte[0], int(minuti))

    def set_intervallo_acqua(self, minuti): #ogni quanti minuti deve esserci il reminder per bere l'acqua
        self.intervallo_acqua=int(minuti)
        print(f"Reminder acqua ogni {minuti} minuti")
        
    def set_ora_mqtt(self, stringa_ora):
        try:
            ore, minuti = map(int, stringa_ora.split(":"))
            self.ora_mqtt = (ore, minuti)
        except:
            print("⚠️ Formato ora non valido:", stringa_ora)        #da levare

    def _ora_in_minuti(self, orario): #conversione dell'orario da ora a minuti a partire da mezzanotte : l'una di notte = 60 minuti ecc
        h, m = orario
        return h * 60 + m

    def controlla_modalita(self):
        ora = self.ora_mqtt #prendo l'ora corrente
        ora_min = self._ora_in_minuti(ora) #converto in minuti l'ora corrente
        notte_min = self._ora_in_minuti(self.ora_notte) #converte in minuti l'ora da cui parte la modalità notte
        giorno_min = self._ora_in_minuti(self.ora_sveglia) #converte in minuti l'ora della sveglia

        if notte_min > giorno_min: #caso classico in cui la notte passa la mezzanotte tipo 23:00 - 7:00, sono durante la modalità notte
            if ora_min >= notte_min or ora_min < giorno_min:
                self.modalita = "notte"
            else:
                self.modalita = "giorno"
        else:#caso in cui la notte non passa la mezzanotte tipo dalle 20 alle 23
            if notte_min <= ora_min < giorno_min:
                self.modalita = "notte"
            else:
                self.modalita = "giorno"

        return self.modalita

    def sveglia_attiva(self):
        # Restituisce True se è l'orario della sveglia
        return self.ora_mqtt == self.ora_sveglia
        
    def promemoria_acqua(self):
        if self.modalita == "notte":
            return False
        if self.ultimo_promemoria_acqua is None:
            # primo giro: parte il conteggio da adesso
            self.ultimo_promemoria_acqua = self.ora_mqtt
            return False

        ora_attuale = self._ora_in_minuti(self.ora_mqtt)
        ultimo = self._ora_in_minuti(self.ultimo_promemoria_acqua)

        # % 1440 gestisce il passaggio della mezzanotte
        if (ora_attuale - ultimo) % (24 * 60) >= self.intervallo_acqua:
            self.ultimo_promemoria_acqua = self.ora_mqtt
            self.promemoria_acqua_totali += 1
            return True

        return False



    def aggiorna(self):
        self.controlla_modalita()

        if self.modalita == "giorno":
            if self.sveglia_attiva() and not self.sveglia_gestita:
                print("Sveglia attiva")
                self.allarme.play(self.allarme.melodia_sveglia, 150, 512)
                self.sveglia_suonando = True
                self.sveglia_gestita = True  # blocca fino al minuto successivo

        if self.promemoria_acqua():
            _thread.start_new_thread(self.allarme.play_once, (self.allarme.melodia_acqua, 150, 512))
            self.display.mostra_promemoria_acqua()
            print("È ora di bere")


        # Reset sveglia_gestita quando cambia minuto
        if not self.sveglia_attiva() and self.sveglia_gestita:
            print("Orario sveglia passato, resetto flag")
            self.sveglia_suonando = False
            self.sveglia_gestita = False

                
    def ferma_sveglia(self):
        if self.sveglia_suonando:
            self.allarme.stop()
            self.sveglia_suonando = False
            print("Sveglia fermata")

    

