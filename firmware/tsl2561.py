from machine import I2C
import time

TSL2561_ADDR = 0x39

CMD = 0x80
CTRL = 0x00
TIMING = 0x01
DATA0LOW = 0x0C
DATA0HIGH = 0x0D
DATA1LOW = 0x0E
DATA1HIGH = 0x0F
POWER_UP = 0x03
POWER_DOWN = 0x00

class TSL2561:
    def __init__(self, i2c, addr=TSL2561_ADDR):
        self.i2c = i2c
        self.addr = addr
        if addr not in self.i2c.scan():
            raise Exception("TSL2561 non trovato all'indirizzo %s" % hex(addr))
        self._power(True)
        self.i2c.writeto_mem(self.addr, CMD | TIMING, b'\x02')  # Integration time = 402ms

    def _power(self, on):
        val = POWER_UP if on else POWER_DOWN
        self.i2c.writeto_mem(self.addr, CMD | CTRL, bytes([val]))

    def read_raw(self):
        ch0 = self.i2c.readfrom_mem(self.addr, CMD | DATA0LOW, 1)[0]
        ch0 |= self.i2c.readfrom_mem(self.addr, CMD | DATA0HIGH, 1)[0] << 8
        ch1 = self.i2c.readfrom_mem(self.addr, CMD | DATA1LOW, 1)[0]
        ch1 |= self.i2c.readfrom_mem(self.addr, CMD | DATA1HIGH, 1)[0] << 8
        return ch0, ch1

    def read_lux(self):
        ch0, ch1 = self.read_raw()
        if ch0 == 0:
            return 0
        ratio = ch1 / ch0
        if ratio <= 0.5:
            lux = 0.0304 * ch0 - 0.062 * ch0 * (ratio ** 1.4)
        elif ratio <= 0.61:
            lux = 0.0224 * ch0 - 0.031 * ch1
        elif ratio <= 0.8:
            lux = 0.0128 * ch0 - 0.0153 * ch1
        elif ratio <= 1.3:
            lux = 0.00146 * ch0 - 0.00112 * ch1
        else:
            lux = 0
        return int(lux)
