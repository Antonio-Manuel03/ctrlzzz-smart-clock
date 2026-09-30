# Ctrl-ZZZ · Smart Clock

Sveglia smart basata su **ESP32** (MicroPython) che controlla una stanza in miniatura: luce, tenda, porta e climatizzazione cambiano in base all'ora, alla modalità giorno/notte e ai sensori. Tutto comunica via **MQTT**, quindi la sveglia si può configurare e monitorare da remoto.

Progetto sviluppato durante la laurea triennale in Ingegneria Informatica (Università di Salerno). Per la dimostrazione è stata costruita una stanza in miniatura con tutti i dispositivi collegati.

## Cosa fa

- **Sveglia** con melodia sul buzzer, fermabile con un pulsante. Orari di sveglia e di notte configurabili via MQTT.
- **Modalità giorno/notte** calcolata dagli orari impostati (gestisce anche il passaggio della mezzanotte).
- **Luce:** di giorno si accende se la luminosità scende sotto una soglia; di notte resta spenta.
- **Tenda:** si apre di giorno e si chiude di notte (servo).
- **Porta:** si apre di giorno; di notte si chiude solo se il sensore IR rileva che è al suo posto. Un pulsante la apre a mano.
- **Ventola / climatizzazione:** raffredda sopra la soglia alta (LED blu) e scalda sotto la soglia bassa (LED rosso).
- **Promemoria acqua** a intervalli regolabili, con animazione sul display e melodia dedicata.
- **Display OLED** con ora, temperatura e icone di stato (modalità, porta, ventola, Wi-Fi), più logo animato all'avvio.
- **Statistiche** pubblicate via MQTT: ore di sonno, promemoria acqua totali, temperatura, luminosità.

## Hardware

| Componente | Funzione | Interfaccia |
|---|---|---|
| ESP32 | microcontrollore | - |
| SSD1306 128x64 | display OLED | I2C (bus 0: SCL 22, SDA 21) |
| TSL2561 | sensore di luminosità | I2C (bus 1: SCL 18, SDA 19) |
| DHT22 | temperatura | GPIO 14 |
| Sensore IR HW-S11 | presenza della porta | GPIO 5 |
| Servo | porta | PWM, GPIO 23 |
| Servo | tenda | PWM, GPIO 26 |
| Ventola (motore) | raffreddamento/riscaldamento | GPIO 12 |
| LED blu / rosso | stato della ventola | GPIO 4 / GPIO 16 |
| LED lampadario | luce della stanza | GPIO 17 |
| Buzzer | sveglia e promemoria | PWM, GPIO 27 |
| Pulsante porta / sveglia | apertura porta / stop sveglia | GPIO 33 / GPIO 32 (con interrupt) |

## Architettura del software

Un modulo per ogni componente, coordinati da `main.py`.

| File | Ruolo |
|---|---|
| `boot.py` | connessione Wi-Fi e MQTT all'avvio, con animazione del logo |
| `main.py` | inizializzazione, callback MQTT e ciclo principale |
| `sveglia.py` | orari, modalità giorno/notte, promemoria acqua, durata del sonno |
| `luce.py`, `tenda.py`, `porta.py`, `ventola.py` | attuatori, ciascuno con la sua logica |
| `allarme.py` | buzzer con melodie via PWM, in un thread separato |
| `pulsante.py` | pulsanti con interrupt e anti-rimbalzo |
| `display.py` | interfaccia OLED |
| `temperatura.py`, `sensore_ir.py`, `tsl2561.py` | driver dei sensori |
| `ssd1306.py`, `ssd1306digits.py` | driver del display |
| `stato.py` | stato condiviso (Wi-Fi e client MQTT) |

## Topic MQTT

**In ascolto** (per configurare la sveglia):

| Topic | Valore |
|---|---|
| `home/time` | ora corrente, formato `HH:MM` |
| `home/sveglia/giorno/ore`, `home/sveglia/giorno/minuti` | orario della sveglia |
| `home/sveglia/notte/ore`, `home/sveglia/notte/minuti` | orario di inizio modalità notte |
| `home/sveglia/acqua` | intervallo del promemoria acqua, in minuti |
| `home/condizionatore/soglia/alta`, `home/condizionatore/soglia/bassa` | soglie di temperatura della ventola |
| `home/luci/soglia` | soglia di luminosità per accendere la luce (0-100) |

**Pubblicati:**

| Topic | Valore |
|---|---|
| `home/sensori/temperatura` | temperatura in °C |
| `home/luminosita` | luminosità in % |
| `home/modalita` | `giorno` oppure `notte` |
| `home/sonno/ore`, `home/sonno/minuti` | durata del sonno tra modalità notte e sveglia |
| `home/acqua/totali` | promemoria acqua scattati |

## Come usarlo

1. Installa MicroPython sull'ESP32 e collega i componenti secondo la tabella sopra.
2. Copia `firmware/config.example.py` in `firmware/config.py` e inserisci Wi-Fi e indirizzo del broker MQTT. Questo file è nel `.gitignore` e non viene caricato.
3. Avvia un broker MQTT (per esempio Mosquitto) sulla stessa rete.
4. Carica tutti i file di `firmware/` sulla scheda, per esempio con `mpremote`:
   ```bash
   cd firmware
   mpremote cp *.py :
   ```
5. Riavvia la scheda. Pubblica l'ora su `home/time` e modifica gli orari dagli altri topic.

## Tecnologie

MicroPython · ESP32 · MQTT (`umqtt`) · I2C · PWM · interrupt · thread (`_thread`)
