from machine import ADC
from config import LIGHT_LOW_THRESHOLD, LIGHT_DARK_VALUE, LIGHT_BRIGHT_VALUE

class LightSensor:
    """Light Dependent Resistor (LDR) sensor for ambient light detection"""
    
    def __init__(self, pinNumber):
        self.analogDigitalConverter = ADC(pinNumber)
    
    def readRaw(self, samples=10):
        """Read raw ADC value averaged over multiple samples"""
        return sum(self.analogDigitalConverter.read_u16() for _ in range(samples)) // samples

    def isItBright(self):
        """Check if ambient light is above threshold (bright enough)"""
        raw = self.readRaw()
        return raw > LIGHT_LOW_THRESHOLD
    
    def isItDark(self):
        """Check if ambient light is below threshold (needs grow light)"""
        return not self.isItBright()
    
    def getLightLevelPercent(self):
        """Get light level as percentage (0-100)"""
        raw = self.readRaw()
        # Clamp to calibration range
        if raw <= LIGHT_DARK_VALUE:
            return 0.0
        elif raw >= LIGHT_BRIGHT_VALUE:
            return 100.0
        else:
            # Linear interpolation
            return ((raw - LIGHT_DARK_VALUE) / (LIGHT_BRIGHT_VALUE - LIGHT_DARK_VALUE)) * 100.0
