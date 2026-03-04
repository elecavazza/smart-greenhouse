from machine import ADC
from config import LIGHT_LOW_THRESHOLD, LIGHT_DARK_VALUE, LIGHT_BRIGHT_VALUE

class LightSensor:
    """Light Dependent Resistor (LDR) sensor for ambient light detection"""
    
    def __init__(self, pinNumber):
        self.analogDigitalConverter = ADC(pinNumber)
        self._lastRawValue = 0
        print(f"[LIGHT_SENSOR] Initialized on ADC pin {pinNumber}")
        print(f"[LIGHT_SENSOR] Threshold: {LIGHT_LOW_THRESHOLD}, Dark: {LIGHT_DARK_VALUE}, Bright: {LIGHT_BRIGHT_VALUE}")
    
    def readRaw(self, samples=10):
        """Read raw ADC value averaged over multiple samples"""
        self._lastRawValue = sum(self.analogDigitalConverter.read_u16() for _ in range(samples)) // samples
        return self._lastRawValue

    def isItBright(self, rawValue=None):
        """Check if ambient light is above threshold (bright enough)"""
        if rawValue is None:
            rawValue = self.readRaw()
        result = rawValue > LIGHT_LOW_THRESHOLD
        print(f"[LIGHT_SENSOR] isItBright: raw={rawValue} > threshold={LIGHT_LOW_THRESHOLD} -> {result}")
        return result
    
    def isItDark(self, rawValue=None):
        """Check if ambient light is below threshold (needs grow light)"""
        if rawValue is None:
            rawValue = self.readRaw()
        result = rawValue <= LIGHT_LOW_THRESHOLD
        print(f"[LIGHT_SENSOR] isItDark: raw={rawValue} <= threshold={LIGHT_LOW_THRESHOLD} -> {result}")
        return result
    
    def getLightLevelPercent(self, rawValue=None):
        """Get light level as percentage (0-100)"""
        if rawValue is None:
            rawValue = self.readRaw()
        # Clamp to calibration range
        if rawValue <= LIGHT_DARK_VALUE:
            return 0.0
        elif rawValue >= LIGHT_BRIGHT_VALUE:
            return 100.0
        else:
            # Linear interpolation
            return ((rawValue - LIGHT_DARK_VALUE) / (LIGHT_BRIGHT_VALUE - LIGHT_DARK_VALUE)) * 100.0
