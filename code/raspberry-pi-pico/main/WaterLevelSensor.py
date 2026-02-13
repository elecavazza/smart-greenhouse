from machine import ADC

LOW_WATER_LEVEL = 15000

class WaterLevelSensor:
    def __init__(self, pinNumber):
        self.analogDigitalConverter = ADC(pinNumber)
    
    def readRaw(self, samples = 10):
        return sum(self.analogDigitalConverter.read_u16() for _ in range(samples)) // samples

    def hasWater(self):
        raw = self.readRaw()
        return raw > LOW_WATER_LEVEL
