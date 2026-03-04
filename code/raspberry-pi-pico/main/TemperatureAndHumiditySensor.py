from machine import Pin, I2C
import time

ADDRESS = 0x38

class TemperatureAndHumiditySensor:
    """
    Driver for AHT21 temperature and humidity sensor.
    
    Wiring (using VIN, GND, SCL, SDA pins):
    - VIN -> 3.3V or 5V
    - GND -> GND
    - SCL -> I2C clock pin
    - SDA -> I2C data pin
    """
    
    def __init__(self, serialClockLinePinNumber, serialDataLinePinNumber):
        self.i2c = I2C(0, scl=Pin(serialClockLinePinNumber), sda=Pin(serialDataLinePinNumber))
        time.sleep_ms(40)
        self._initialize()

    def _initialize(self):
        """Initialize and calibrate the AHT21 sensor."""
        # Send calibration command
        self.i2c.writeto(ADDRESS, bytes([0xBE, 0x08, 0x00]))
        time.sleep_ms(100)
        
        # Check calibration status
        self.i2c.writeto(ADDRESS, bytes([0x71]))
        status = self.i2c.readfrom(ADDRESS, 1)
        
        if not (status[0] & 0x68) == 0x08:
            raise Exception("AHT21 initialization failed!")

    def read(self):
        """Read temperature and humidity from the sensor.
        
        Returns:
            tuple: (temperature in Celsius, humidity percentage)
        """
        # Trigger measurement
        self.i2c.writeto(ADDRESS, b'\xAC\x33\x00')
        time.sleep_ms(80)

        data = self.i2c.readfrom(ADDRESS, 6)

        raw_humidity = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        raw_temperature = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

        humidity = raw_humidity * 100 / 1048576
        temperature = raw_temperature * 200 / 1048576 - 50

        return temperature, humidity
