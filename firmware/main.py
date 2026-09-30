from sveglia import Sveglia
from ventola import Ventola
from tenda import Tenda
from luce import Luce
from porta import Porta
from pulsante import Pulsante
from allarme import Allarme
from display import Display
from temperatura import SensoreTemperatura
from stato import mqtt_client, wifi_connessa
from time import sleep, localtime

# === Inizializzazione pin ===
pinventola = 12 #motore ventola
pin_led_blu = 4
pin_led_rosso = 16
pinluce = 17 #led lampadario
pinporta = 23 #servo porta 
pintenda = 26 #servo tenda
pintemperatura = 14 #sensore temperatura
pin_sensore_porta = 5 #sensore distanza
pinallarme = 27 #buzzer
pinpulsanteporta = 33
pinpulsantesveglia = 32

# === Inizializzazione componenti ===
allarme = Allarme(pinallarme)
allarme.stop()
tenda = Tenda(pintenda)
luce = Luce(pinluce)
ventola = Ventola(pinventola,pin_led_blu,pin_led_rosso,allarme)
porta = Porta(pinporta, pin_sensore_porta)
display = Display()
sveglia = Sveglia(allarme, display)
sensore_temperatura = SensoreTemperatura(pintemperatura)



# === Callback MQTT ===
def mqtt_callback(topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    print(f"[MQTT] {topic} → {msg}")

    if topic == "home/time":
        sveglia.set_ora_mqtt(msg)  # msg è tipo "14:38"

    elif topic == "home/sveglia/giorno/ore":
        sveglia.set_ora_sveglia_ore(msg)

    elif topic == "home/sveglia/giorno/minuti":
        sveglia.set_ora_sveglia_minuti(msg)

    elif topic == "home/sveglia/notte/ore":
        sveglia.set_ora_notte_ore(msg)

    elif topic == "home/sveglia/notte/minuti":
        sveglia.set_ora_notte_minuti(msg)

    elif topic == "home/sveglia/acqua":
        try:
            intervallo = int(msg)
            sveglia.set_intervallo_acqua(intervallo)
        except:
            print("Intervallo acqua non valido:", msg)

    elif topic == "home/condizionatore/soglia/alta":
        try:
            ventola.set_soglia_alta(float(msg))
        except:
            print("Valore soglia non valido:", msg)

    elif topic == "home/condizionatore/soglia/bassa":
        try:
            ventola.set_soglia_bassa(float(msg))
        except:
            print("Valore soglia non valido:", msg)

    elif topic == "home/luci/soglia":
        try:
            luce.set_soglia(int(msg))
        except:
            print("Valore soglia non valido:", msg)
            
def apri_porta_callback():
    print("Pulsante premuto → apro la porta")
    porta.apri()

def ferma_sveglia_callback():
    print("Pulsante sveglia premuto → fermo la sveglia")
    sveglia.ferma_sveglia()

# === Configura client MQTT ===
if mqtt_client:
    mqtt_client.set_callback(mqtt_callback)
    mqtt_client.subscribe(b"home/time")
    mqtt_client.subscribe(b"home/sveglia/#")
    mqtt_client.subscribe(b"home/condizionatore/soglia/alta")
    mqtt_client.subscribe(b"home/condizionatore/soglia/bassa")
    mqtt_client.subscribe(b"home/luci/soglia")
    print("MQTT pronto e sottoscritto a 'home/#'")
else:
    print("⚠️ MQTT non disponibile, impossibile sottoscriversi.")


# === Ciclo principale ===
temperatura = sensore_temperatura.leggi()
luminosita = luce.get_luminosita()
ora = sveglia.get_ora_corrente()
ventola_attiva =ventola.get_ventola_attiva()
modalita = sveglia.get_modalita()
porta_aperta = porta.get_porta_aperta()
wifi = wifi_connessa()
pulsante_porta = Pulsante(pinpulsanteporta, apri_porta_callback)
pulsante_sveglia = Pulsante(pinpulsantesveglia, ferma_sveglia_callback)


last_sonno = (-1, -1) 
last_acqua_totali = -1
last_lum = 0
last_mod = modalita
last_temp = 0



while True:


    for _ in range(20):  # o un numero più alto, se vuoi essere più sicuro
        if mqtt_client:
            try:
                mqtt_client.check_msg()
            except Exception as e:
                print("❌ Errore MQTT:", e)
                mqtt_client = None  # forza la riconnessione se vuoi
        else:
            print("⚠️ MQTT non disponibile al momento.")

        sleep(0.01)  # piccolo delay per non sovraccaricare la CPU



    sveglia.aggiorna()
    temperatura = sensore_temperatura.leggi()
    luminosita = luce.get_luminosita()
    ora = sveglia.get_ora_corrente()
    ventola_attiva =ventola.get_ventola_attiva()
    modalita = sveglia.get_modalita()
    porta_aperta = porta.get_porta_aperta()
    wifi = wifi_connessa()


    ventola.aggiorna(temperatura)
    luce.aggiorna(modalita)
    porta.aggiorna(modalita)
    tenda.aggiorna(modalita)
    display.aggiorna(ora, temperatura, ventola_attiva, porta_aperta, modalita, wifi)
    
    ore_sonno, min_sonno = sveglia.get_durata_sonno()
    totali = sveglia.promemoria_acqua_totali
    
    if (ore_sonno, min_sonno) != last_sonno:
        last_sonno = (ore_sonno, min_sonno)
        try:
            mqtt_client.publish("home/sonno/ore", str(ore_sonno))
            mqtt_client.publish("home/sonno/minuti", str(min_sonno))
            print(f"[MQTT] Ore sonno aggiornate: {ore_sonno}h {min_sonno}m")
        except Exception as e:
            print("❌ Errore publish sonno:", e)
                

    if totali != last_acqua_totali:  # confronta solo il valore totali
        last_acqua_totali = totali # aggiorna tupla anche se il primo valore non si usa più
        try:
            mqtt_client.publish("home/acqua/totali", str(totali))
            print(f"[MQTT] Promemoria acqua totali aggiornato: {totali}")
        except Exception as e:
            print("❌ Errore publish acqua:", e)


    if temperatura != last_temp:
        if mqtt_client:
            try:
                mqtt_client.publish("home/sensori/temperatura", str(temperatura))
            except Exception as e:
                print("❌ Errore nel publish MQTT:", e)
                mqtt_client = None  # puoi anche tentare ricollegamento qui
        else:
            print("⚠️ MQTT non connesso: publish ignorato.")
        last_temp = temperatura
        
    if luminosita != last_lum:
        if mqtt_client:
            try:
                mqtt_client.publish("home/luminosita", str(luminosita))
            except Exception as e:
                print("❌ Errore nel publish MQTT:", e)
                mqtt_client = None  # puoi anche tentare ricollegamento qui
        else:
            print("⚠️ MQTT non connesso: publish ignorato.")
        last_lum= luminosita
        


    if modalita != last_mod:
        if mqtt_client:
            try:
                mqtt_client.publish("home/modalita", modalita)
            except Exception as e:
                print("❌ Errore nel publish MQTT:", e)
                mqtt_client = None  # puoi anche tentare ricollegamento qui
        else:
            print("⚠️ MQTT non connesso: publish ignorato.")
        last_mod = modalita
        
    last_lum = luminosita
    last_mod = modalita
    last_temp = temperatura


    sleep(5)
