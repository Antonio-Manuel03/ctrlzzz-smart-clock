from machine import Pin, I2C
from time import sleep
import framebuf
import ssd1306
import ssd1306digits  # nuovo driver ottimizzato
from logoboot import cup1, cup2, cup3, cup4, cup5, cup6, cup7, cup8, cup9

class Display:
    def __init__(self, SCL_PIN=22, SDA_PIN=21):
        self.width = 128
        self.height = 64
        self.i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
        self.display = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
        self.display.fill(0)
        ssd1306digits.set_display(self.display)
        self.display.show()

    def display_centrato(self, text, y):
        ssd1306digits.draw_time(text, y)
    
    def mostra_logo(self, fb):
        self.display.fill(0)
        self.display.blit(fb, 0, 0)
        self.display.show()
        
    def mostra_promemoria_acqua(self, ripetizioni=3, delay=0.2):
        frames = [
            framebuf.FrameBuffer(cup1, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup2, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup3, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup4, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup5, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup6, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup7, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup8, 128, 64, framebuf.MONO_HLSB),
            framebuf.FrameBuffer(cup9, 128, 64, framebuf.MONO_HLSB),
        ]

        for _ in range(ripetizioni):
            for fb in frames:
                self.display.fill(0)
                self.display.blit(fb, 8, 0)
                self.display.show()
                sleep(delay)

        # Dopo il promemoria, pulisce il display
        self.display.fill(0)
        self.display.show()


    def aggiorna(self, ora_corrente, temperatura, condizionatore_attivo, porta_aperta, modalita, wifi_connessa):
        # Icone (12x12 pixel)
        wifi = b'\x00\x00\x1f\x80\x79\xe0\xc6\x30\x1f\x80\x30\xc0\x0f\x00\x09\x00\x06\x00\x0f\x00\x06\x00\x00\x00'
        sole = b'\x00\x00\x06\x00\x20\xc0\x36\x80\x0f\x00\x5f\xa0\x5f\xa0\x0f\x00\x36\x80\x20\xc0\x06\x00\x00\x00'
        luna = b'\x10\x00\x30\x00\x60\x00\xe0\x00\xe0\x00\xe0\x00\xe0\x00\xf0\x10\x78\x30\x7f\xe0\x3f\xc0\x0f\x80'
        lucchetto_chiuso = b'\x0f\x00\x19\x80\x30\xc0\x30\xc0\x30\xc0\x30\xc0\x3f\xe0\x7f\xe0\x79\xe0\x79\xe0\x7d\xe0\x3f\xc0'
        lucchetto_aperto = b'\x0f\x00\x19\x80\x30\xc0\x20\xc0\x00\xc0\x00\xc0\x3f\xc0\x7f\xe0\x79\xe0\x79\xe0\x7d\xe0\x3f\xc0'
        ventola = b'\x06\x00\x0f\x00\x0f\x00\x0e\x00\x64\xe0\xf7\xf0\xfe\xf0\x72\x60\x07\x00\x0f\x00\x0f\x00\x06\x00'

        # Pulisce lo schermo
        self.display.fill(0)

        # Orario centrato in grande
        ora_str = "{:02}:{:02}".format(ora_corrente[0], ora_corrente[1])
        self.display_centrato(ora_str, 24)

        # Icona sole/luna
        icona_luce = sole if modalita == "giorno" else luna
        fb1 = framebuf.FrameBuffer(bytearray(icona_luce), 12, 12, framebuf.MONO_HLSB)
        self.display.blit(fb1, 0, 0)

        # Temperatura in alto a destra
        temp_str = "{}C".format(int(temperatura)) if temperatura is not None else "--"
        self.display.text(temp_str, self.width - len(temp_str) * 8, 0)

        # Icona ventola se attivo
        if condizionatore_attivo:
            fb2 = framebuf.FrameBuffer(bytearray(ventola), 12, 12, framebuf.MONO_HLSB)
            self.display.blit(fb2, 39, 0)

        # Icona porta
        icona_lucchetto = lucchetto_aperto if porta_aperta else lucchetto_chiuso
        fb3 = framebuf.FrameBuffer(bytearray(icona_lucchetto), 12, 12, framebuf.MONO_HLSB)
        self.display.blit(fb3, 13, 0)

        # Icona Wi-Fi se connesso
        if wifi_connessa:
            fb4 = framebuf.FrameBuffer(bytearray(wifi), 12, 12, framebuf.MONO_HLSB)
            self.display.blit(fb4, 26, 0)

        # Mostra tutto
        self.display.show()

