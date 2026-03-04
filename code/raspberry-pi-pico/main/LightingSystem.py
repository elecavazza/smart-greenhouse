"""
Lighting System Module
Manages grow light based on ambient light levels
"""

from Relay import Relay
from LightSensor import LightSensor
from config import LIGHT_RELAY_PIN, LIGHT_SENSOR_PIN, LIGHT_LOW_THRESHOLD


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
        print(f"[LIGHTING] Initializing with relay on GP{LIGHT_RELAY_PIN}, sensor on ADC{LIGHT_SENSOR_PIN}")
        # LED relay uses active-HIGH logic (opposite of other relays)
        self.light = Relay(LIGHT_RELAY_PIN, "GROW_LIGHT", active_low=True)
        self.sensor = LightSensor(LIGHT_SENSOR_PIN)
        
        # System state
        self.enabled = True  # System on/off (controlled by UI)
        self.isLightOn = False  # Current light state
        
        # Ensure light is off at startup
        print("[LIGHTING] Setting initial state: Light OFF")
        self.light.turnOff()
        print("[LIGHTING] System initialized - Light OFF")
    
    def enable(self):
        """Enable the lighting system (automatic control active)"""
        self.enabled = True
        print("[LIGHTING] System ENABLED - automatic control active")
    
    def disable(self):
        """Disable the lighting system (light off, no auto control)"""
        self.enabled = False
        self._setLight(False)
        print("[LIGHTING] System DISABLED - light turned OFF")
    
    def update(self):
        """
        Run automatic lighting logic (called from main loop).
        Turns on grow light when ambient light is low.
        """
        if not self.enabled:
            print("[LIGHTING] System disabled, skipping update")
            return
        
        # Read sensor value ONCE and use it for all operations
        rawValue = self.sensor.readRaw()
        lightPercent = self.sensor.getLightLevelPercent(rawValue)
        isDark = self.sensor.isItDark(rawValue)
        
        # Log sensor readings
        print(f"[LIGHTING] === Update ===")
        print(f"[LIGHTING] LDR raw: {rawValue}")
        print(f"[LIGHTING] Light level: {lightPercent:.1f}%")
        print(f"[LIGHTING] Is dark: {isDark} (threshold: {LIGHT_LOW_THRESHOLD})")
        print(f"[LIGHTING] Current light state: {'ON' if self.isLightOn else 'OFF'}")
        
        # Check if it's dark enough to need grow light
        previousState = self.isLightOn
        if isDark:
            print(f"[LIGHTING] Dark detected, turning light ON")
            self._setLight(True)
        else:
            print(f"[LIGHTING] Bright detected, turning light OFF")
            self._setLight(False)
        
        # Log state change
        if previousState != self.isLightOn:
            print(f"[LIGHTING] *** STATE CHANGED: Light {'ON' if self.isLightOn else 'OFF'} ***")
        else:
            print(f"[LIGHTING] State unchanged: Light {'ON' if self.isLightOn else 'OFF'}")
    
    def _setLight(self, on):
        """Set light state and update tracking variable"""
        print(f"[LIGHTING] _setLight called with on={on}, current isLightOn={self.isLightOn}")
        if on:
            print("[LIGHTING] Calling relay.turnOn()")
            self.light.turnOn()
            self.isLightOn = True
        else:
            print("[LIGHTING] Calling relay.turnOff()")
            self.light.turnOff()
            self.isLightOn = False
    
    def getLightLevelPercent(self):
        """Get ambient light level as percentage (0-100)"""
        return self.sensor.getLightLevelPercent()
    
    def getStatus(self):
        """Get current system status as string"""
        return f"Enabled: {self.enabled}, Light: {'ON' if self.isLightOn else 'OFF'}, Brightness: {self.getLightLevelPercent():.1f}%"
