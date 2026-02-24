"""
Greenhouse Controller Module
Main orchestrator that coordinates all systems and handles ESP32 communication
"""

import time
from machine import Pin
from UARTCommunication import UARTCommunication
from WateringSystem import WateringSystem
from AirQualitySystem import AirQualitySystem
from LightingSystem import LightingSystem
from config import SENSOR_READ_INTERVAL_MS, DATA_SEND_INTERVAL_MS


class GreenhouseController:
    """
    Main controller that orchestrates all greenhouse systems.
    
    Responsibilities:
    - Initialize all subsystems
    - Run main control loop
    - Process commands from ESP32
    - Send sensor data and status to ESP32
    """
    
    def __init__(self):
        """Initialize all subsystems"""
        print("Initializing Greenhouse Controller...")
        
        # Communication
        self.uart = UARTCommunication()
        
        # Systems
        self.wateringSystem = WateringSystem()
        self.airQualitySystem = AirQualitySystem()
        self.lightingSystem = LightingSystem()
        
        # Status LED (onboard)
        self.led = Pin("LED", Pin.OUT)
        
        # Timing
        self.lastSensorRead = 0
        self.lastDataSend = 0
        
        print("Greenhouse Controller initialized")
    
    def run(self):
        """Main control loop - runs forever"""
        # Signal ready to ESP32
        self.uart.sendReady()
        
        # Initial sensor read and status send
        time.sleep_ms(500)
        self._readAllSensors()
        self.sendAllSensorData()
        self.sendAllStatus()
        
        print("Greenhouse Controller running...")
        
        while True:
            try:
                currentTime = time.ticks_ms()
                
                # Heartbeat LED
                self.led.toggle()
                
                # Process any incoming commands from ESP32
                self._processCommands()
                
                # Read sensors periodically
                if time.ticks_diff(currentTime, self.lastSensorRead) >= SENSOR_READ_INTERVAL_MS:
                    self._readAllSensors()
                    self.lastSensorRead = currentTime
                
                # Update all systems (run automatic control logic)
                self._updateSystems()
                
                # Send data to ESP32 periodically
                if time.ticks_diff(currentTime, self.lastDataSend) >= DATA_SEND_INTERVAL_MS:
                    self.sendAllSensorData()
                    self.lastDataSend = currentTime
                
                # Small delay to prevent busy loop
                time.sleep_ms(100)
                
            except Exception as e:
                print(f"Main loop error: {e}")
                # Flash LED rapidly to indicate error
                for _ in range(5):
                    self.led.on()
                    time.sleep_ms(100)
                    self.led.off()
                    time.sleep_ms(100)
    
    def _processCommands(self):
        """Process all pending commands from ESP32"""
        commands = self.uart.receiveAll()
        for cmd in commands:
            self._handleCommand(cmd)
    
    def _handleCommand(self, cmd):
        """Handle a single command from ESP32"""
        print(f"Received command: {cmd}")
        
        # Request commands
        if cmd == "REQ:SENSORS":
            self.sendAllSensorData()
            
        elif cmd == "REQ:STATUS":
            self.sendAllStatus()
        
        # Watering system commands
        elif cmd == "CMD:WATER:ON":
            self.wateringSystem.enable()
            self.uart.sendStatus("WATER", True)
            
        elif cmd == "CMD:WATER:OFF":
            self.wateringSystem.disable()
            self.uart.sendStatus("WATER", False)
        
        # Lighting system commands
        elif cmd == "CMD:LIGHT:ON":
            self.lightingSystem.enable()
            self.uart.sendStatus("LIGHT", True)
            
        elif cmd == "CMD:LIGHT:OFF":
            self.lightingSystem.disable()
            self.uart.sendStatus("LIGHT", False)
        
        # Air quality system commands
        elif cmd == "CMD:AIR:ON":
            self.airQualitySystem.enable()
            self.uart.sendStatus("AIR", True)
            
        elif cmd == "CMD:AIR:OFF":
            self.airQualitySystem.disable()
            self.uart.sendStatus("AIR", False)
        
        else:
            print(f"Unknown command: {cmd}")
    
    def _readAllSensors(self):
        """Read all sensor values (for caching)"""
        # Air quality sensor read is done in update(), but we can force it here
        self.airQualitySystem.readSensor()
    
    def _updateSystems(self):
        """Run automatic control logic for all enabled systems"""
        self.wateringSystem.update()
        self.airQualitySystem.update()
        self.lightingSystem.update()
    
    def sendAllSensorData(self):
        """Send all sensor readings to ESP32"""
        # Temperature
        self.uart.sendSensorData("TEMP", self.airQualitySystem.getTemperature())
        
        # Humidity
        self.uart.sendSensorData("HUMIDITY", self.airQualitySystem.getHumidity())
        
        # Soil moisture
        self.uart.sendSensorData("SOIL", self.wateringSystem.getSoilMoisturePercent())
        
        # Water level
        self.uart.sendSensorData("WATER", self.wateringSystem.getWaterLevelPercent())
    
    def sendAllStatus(self):
        """Send status of all systems to ESP32"""
        self.uart.sendStatus("WATER", self.wateringSystem.enabled)
        self.uart.sendStatus("LIGHT", self.lightingSystem.enabled)
        self.uart.sendStatus("AIR", self.airQualitySystem.enabled)
