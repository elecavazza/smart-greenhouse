"""
Air Quality System Module
Manages ventilation fan based on temperature and humidity readings
"""

from Relay import Relay
from TemperatureAndHumiditySensor import TemperatureAndHumiditySensor
from config import (
    FAN_RELAY_PIN, TEMP_HUMIDITY_SCL, TEMP_HUMIDITY_SDA,
    TEMP_HIGH_THRESHOLD, TEMP_LOW_THRESHOLD,
    HUMIDITY_HIGH_THRESHOLD, HUMIDITY_LOW_THRESHOLD
)


class AirQualitySystem:
    """
    Manages automatic ventilation based on temperature and humidity.
    
    When enabled:
    - Fan ON if temperature > TEMP_HIGH_THRESHOLD (too hot)
    - Fan ON if humidity > HUMIDITY_HIGH_THRESHOLD (too humid)
    - Fan ON if humidity < HUMIDITY_LOW_THRESHOLD (too dry, circulate air)
    - Fan OFF if temperature < TEMP_LOW_THRESHOLD (preserve heat)
    - Fan OFF otherwise (conditions are good)
    
    When disabled:
    - Fan is off
    - No automatic checks run
    """
    
    def __init__(self):
        """Initialize air quality system components"""
        self.fan = Relay(FAN_RELAY_PIN)
        self.sensor = TemperatureAndHumiditySensor(
            serialClockLinePinNumber=TEMP_HUMIDITY_SCL,
            serialDataLinePinNumber=TEMP_HUMIDITY_SDA
        )
        
        # System state
        self.enabled = True  # System on/off (controlled by UI)
        self.isFanOn = False  # Current fan state
        
        # Cached sensor readings
        self._temperature = 0.0
        self._humidity = 0.0
        
        # Ensure fan is off at startup
        self.fan.turnOff()
    
    def enable(self):
        """Enable the air quality system (automatic control active)"""
        self.enabled = True
        print("Air quality system ENABLED")
    
    def disable(self):
        """Disable the air quality system (fan off, no auto control)"""
        self.enabled = False
        self._setFan(False)
        print("Air quality system DISABLED")
    
    def update(self):
        """
        Run automatic ventilation logic (called from main loop).
        Reads sensor and controls fan based on thresholds.
        """
        if not self.enabled:
            return
        
        # Read sensor values
        try:
            self._temperature, self._humidity = self.sensor.read()
        except Exception as e:
            print(f"Error reading temp/humidity sensor: {e}")
            return
        
        # Determine if fan should be on
        shouldFanBeOn = False
        
        # Check temperature
        if self._temperature > TEMP_HIGH_THRESHOLD:
            shouldFanBeOn = True  # Too hot
        elif self._temperature < TEMP_LOW_THRESHOLD:
            shouldFanBeOn = False  # Too cold, preserve heat
        
        # Check humidity (can override temperature decision)
        if self._humidity > HUMIDITY_HIGH_THRESHOLD:
            shouldFanBeOn = True  # Too humid
        elif self._humidity < HUMIDITY_LOW_THRESHOLD:
            shouldFanBeOn = True  # Too dry, circulate air
        
        # Apply fan state
        self._setFan(shouldFanBeOn)
    
    def _setFan(self, on):
        """Set fan state and update tracking variable"""
        if on:
            self.fan.turnOn()
            self.isFanOn = True
        else:
            self.fan.turnOff()
            self.isFanOn = False
    
    def getTemperature(self):
        """Get current temperature in Celsius"""
        return self._temperature
    
    def getHumidity(self):
        """Get current humidity percentage"""
        return self._humidity
    
    def readSensor(self):
        """Force a sensor read and return (temperature, humidity)"""
        try:
            self._temperature, self._humidity = self.sensor.read()
        except Exception as e:
            print(f"Error reading temp/humidity sensor: {e}")
        return self._temperature, self._humidity
