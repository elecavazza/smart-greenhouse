from machine import I2C
import time

AHT30_ADDR = 0x38

class AHT30:
    def __init__(self, i2c):
        self.i2c = i2c
        time.sleep_ms(40)

    def read(self):
        # Trigger measurement
        self.i2c.writeto(AHT30_ADDR, b'\xAC\x33\x00')
        time.sleep_ms(80)

        data = self.i2c.readfrom(AHT30_ADDR, 6)

        raw_humidity = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = raw_humidity * 100 / 1048576
        temperature = raw_temperature * 200 / 1048576 - 50

        return temperature, humidity
