"""
Lighting System Module
Manages grow light based on ambient light levels
"""

from Relay import Relay
from LightSensor import LightSensor
from config import LIGHT_RELAY_PIN, LIGHT_SENSOR_PIN


class LightingSystem:
    """
    Manages automatic grow light control based on ambient light.
    
    When enabled:
    - Light ON if ambient light is low (dark)
    - Light OFF if ambient light is sufficient (bright)
    
    When disabled:
    - Light is off
    - No automatic checks run
    """
    
    def __init__(self):
        """Initialize lighting system components"""
        self.light = Relay(LIGHT_RELAY_PIN)
        self.sensor = LightSensor(LIGHT_SENSOR_PIN)
        
        # System state
        self.enabled = True  # System on/off (controlled by UI)
        self.isLightOn = False  # Current light state
        
        # Ensure light is off at startup
        self.light.turnOff()
    
    def enable(self):
        """Enable the lighting system (automatic control active)"""
        self.enabled = True
        print("Lighting system ENABLED")
    
    def disable(self):
        """Disable the lighting system (light off, no auto control)"""
        self.enabled = False
        self._setLight(False)
        print("Lighting system DISABLED")
    
    def update(self):
        """
        Run automatic lighting logic (called from main loop).
        Turns on grow light when ambient light is low.
        """
        if not self.enabled:
            return
        
        # Check if it's dark enough to need grow light
        if self.sensor.isItDark():
            self._setLight(True)
        else:
            self._setLight(False)
    
    def _setLight(self, on):
        """Set light state and update tracking variable"""
        if on:
            self.light.turnOn()
            self.isLightOn = True
        else:
            self.light.turnOff()
            self.isLightOn = False
    
    def getLightLevelPercent(self):
        """Get ambient light level as percentage (0-100)"""
        return self.sensor.getLightLevelPercent()
