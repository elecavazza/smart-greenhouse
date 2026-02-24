from machine import Pin, I2C
import time

address = 0x38
class TemperatureAndHumiditySensor:
    def __init__(self, serialClockLinePinNumber, serialDataLinePinNumber):
        self.i2c = I2C(0, scl=Pin(serialClockLinePinNumber), sda=Pin(serialDataLinePinNumber))
        time.sleep_ms(40)

    def read(self):
        # Trigger measurement
        self.i2c.writeto(address, b'\xAC\x33\x00')
        time.sleep_ms(80)

        data = self.i2c.readfrom(address, 6)

        raw_humidity = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = raw_humidity * 100 / 1048576
        temperature = raw_temperature * 200 / 1048576 - 50

        return temperature, humidity




while True:
    try:
        sensor = TemperatureAndHumiditySensor(serialClockLinePinNumber = 5, serialDataLinePinNumber = 4)
        temperature, humidty = sensor.read()
        print("Temperature: {:.2f} °C".format(temperature))
        print("Humidity: {:.2f} %".format(humidty))
        print("----------------------")
        time.sleep(2)
    except Exception as e:
        print(f"error: {e}")
        
    
