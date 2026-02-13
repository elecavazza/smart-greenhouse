from machine import ADC

LOW_LIGHT_LEVEL = 1000

class LightLevelSensor:
    def __init__(self, pinNumber):
        self.analogDigitalConverter = ADC(pinNumber)
    
    def readRaw(self, samples = 10):
        return sum(self.analogDigitalConverter.read_u16() for _ in range(samples)) // samples

    def isItBright(self):
        raw = self.readRaw()
        return raw > LOW_LIGHT_LEVEL
