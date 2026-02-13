from machine import ADC

AIR = 65000       # sensor in air (dry)
DRY_SOIL = 50000
MOIST_SOIL = 38000
WET_SOIL = 26000
WATER = 15000     # sensor in water

class SoilMoistureSensor:
    def __init__(self, pinNumber):
        self.analogDigitalConverter = ADC(pinNumber)
    
    def readRaw(self, samples = 10):
        return sum(self.analogDigitalConverter.read_u16() for _ in range(samples)) // samples
        
    
    def readLevel(self):
        raw = self.readRaw()
    
        if raw > AIR:
            return "BONE DRY"
        elif raw > DRY_SOIL:
            return "VERY DRY"
        elif raw > MOIST_SOIL:
            return "DRY"
        elif raw > WET_SOIL:
            return "MOIST"
        elif raw > WATER:
            return "WET"
        else:
            return "SOAKED"

    def isItDry(self):
        raw = self.readRaw()
        return raw > MOIST_SOIL

    