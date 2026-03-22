"""
Watering System Module
Manages water pump with pulse watering, soil moisture sensor, and water level sensor
"""

import time
from Relay import Relay
from SoilMoistureSensor import SoilMoistureSensor
from WaterLevelSensor import WaterLevelSensor
from config import (
    PUMP_RELAY_PIN, SOIL_MOISTURE_PIN, WATER_LEVEL_PIN,
    SOIL_DRY_THRESHOLD, WATER_LOW_THRESHOLD,
    PUMP_PULSE_MS, PUMP_COOLDOWN_MS,
    SOIL_AIR_VALUE, SOIL_WATER_VALUE,
    WATER_EMPTY_VALUE, WATER_FULL_VALUE
)


class WateringSystem:
    """
    Manages automatic watering with pulse-based irrigation.
    
    When enabled:
    - Checks if soil is dry
    - Checks if reservoir has water
    - Pumps for a short burst (PUMP_PULSE_MS)
    - Waits for cooldown period before next pulse
    
    When disabled:
    - Pump is off
    - No automatic checks run
    """
    
    def __init__(self):
        """Initialize watering system components"""
        self.pump = Relay(PUMP_RELAY_PIN, "PUMP")
        self.soilSensor = SoilMoistureSensor(SOIL_MOISTURE_PIN)
        self.waterLevelSensor = WaterLevelSensor(WATER_LEVEL_PIN)
        
        # System state
        self.enabled = False  # System on/off (controlled by UI)
        self.lastPulseTime = 0  # Timestamp of last pump pulse
        self.isPumping = False  # Current pump state
        
        # Ensure pump is off at startup
        self.pump.turnOff()
        print("[WATERING] System initialized - Pump OFF")
    
    def enable(self):
        """Enable the watering system (automatic control active)"""
        self.enabled = True
        print("[WATERING] System ENABLED - automatic control active")
    
    def disable(self):
        """Disable the watering system (pump off, no auto control)"""
        self.enabled = False
        self.pump.turnOff()
        self.isPumping = False
        print("[WATERING] System DISABLED - pump turned OFF")
    
    def update(self):
        """
        Run automatic watering logic (called from main loop).
        Uses pulse watering: short bursts with cooldown period.
        """
        if not self.enabled:
            return
        
        # Read sensor values
        soilRaw = self.soilSensor.readRaw()
        soilPercent = self.getSoilMoisturePercent()
        waterRaw = self.waterLevelSensor.readRaw()
        waterPercent = self.getWaterLevelPercent()
        isDry = self.isSoilDry()
        hasWater = self.hasWater()
        
        # Log sensor readings
        print(f"[WATERING] Soil raw: {soilRaw}, Moisture: {soilPercent:.1f}%, Dry: {isDry}, Threshold: {SOIL_DRY_THRESHOLD}")
        print(f"[WATERING] Water raw: {waterRaw}, Level: {waterPercent:.1f}%, HasWater: {hasWater}, Threshold: {WATER_LOW_THRESHOLD}")
        
        # Check if soil needs water
        if not isDry:
            print("[WATERING] Soil is moist enough - no watering needed")
            return
        
        # Check if reservoir has water
        if not hasWater:
            print("[WATERING] WARNING: Reservoir is low on water! Cannot water.")
            return
        
        # Check if cooldown period has passed
        currentTime = time.ticks_ms()
        timeSinceLastPulse = time.ticks_diff(currentTime, self.lastPulseTime)
        cooldownRemaining = PUMP_COOLDOWN_MS - timeSinceLastPulse
        
        if timeSinceLastPulse < PUMP_COOLDOWN_MS:
            print(f"[WATERING] Cooldown active - {cooldownRemaining}ms remaining")
            return
        
        # Perform pulse watering
        print(f"[WATERING] Soil is dry, reservoir OK - starting pulse")
        self.pulse()
    
    def pulse(self):
        """Run pump for a short burst (PUMP_PULSE_MS)"""
        print(f"[WATERING] PUMP ON - pulsing for {PUMP_PULSE_MS}ms")
        self.isPumping = True
        self.pump.turnOn()
        time.sleep_ms(PUMP_PULSE_MS)
        self.pump.turnOff()
        self.isPumping = False
        self.lastPulseTime = time.ticks_ms()
        print(f"[WATERING] PUMP OFF - cooldown started ({PUMP_COOLDOWN_MS}ms)")
    
    def isSoilDry(self):
        """Check if soil moisture is below threshold (needs water)"""
        return self.soilSensor.isItDry()
    
    def hasWater(self):
        """Check if reservoir has enough water"""
        return self.waterLevelSensor.hasWater()
    
    def getSoilMoisturePercent(self):
        """
        Get soil moisture as percentage (0-100).
        0% = bone dry, 100% = soaking wet
        Note: Raw ADC is inverted (higher = drier)
        """
        raw = self.soilSensor.readRaw()
        
        # Clamp to calibration range
        if raw >= SOIL_AIR_VALUE:
            return 0.0  # Completely dry
        elif raw <= SOIL_WATER_VALUE:
            return 100.0  # Soaking wet
        else:
            # Inverted linear interpolation (higher raw = lower moisture)
            return ((SOIL_AIR_VALUE - raw) / (SOIL_AIR_VALUE - SOIL_WATER_VALUE)) * 100.0
    
    def getWaterLevelPercent(self):
        """
        Get water level as percentage (0-100).
        0% = empty, 100% = full
        """
        raw = self.waterLevelSensor.readRaw()
        
        # Clamp to calibration range
        if raw <= WATER_EMPTY_VALUE:
            return 0.0  # Empty
        elif raw >= WATER_FULL_VALUE:
            return 100.0  # Full
        else:
            # Linear interpolation
            return ((raw - WATER_EMPTY_VALUE) / (WATER_FULL_VALUE - WATER_EMPTY_VALUE)) * 100.0
    
    def getStatus(self):
        """Get current system status as string"""
        return f"Enabled: {self.enabled}, Pumping: {self.isPumping}, Soil: {self.getSoilMoisturePercent():.1f}%, Water: {self.getWaterLevelPercent():.1f}%"
