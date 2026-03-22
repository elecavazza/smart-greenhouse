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
        print("=" * 50)
        print("[CONTROLLER] Initializing Greenhouse Controller...")
        print("=" * 50)
        
        # Communication
        print("[CONTROLLER] Setting up UART communication...")
        self.uart = UARTCommunication()
        
        # Systems
        print("[CONTROLLER] Initializing Watering System...")
        self.wateringSystem = WateringSystem()
        
        print("[CONTROLLER] Initializing Air Quality System...")
        self.airQualitySystem = AirQualitySystem()
        
        print("[CONTROLLER] Initializing Lighting System...")
        self.lightingSystem = LightingSystem()
        
        # Status LED (onboard)
        self.led = Pin("LED", Pin.OUT)
        
        # Timing
        self.lastSensorRead = 0
        self.lastDataSend = 0
        self.loopCount = 0
        
        print("=" * 50)
        print("[CONTROLLER] Greenhouse Controller initialized!")
        print("=" * 50)
    
    def run(self):
        """Main control loop - runs forever"""
        # Signal ready to ESP32
        print("[CONTROLLER] Sending READY signal to ESP32...")
        self.uart.sendReady()
        
        # Initial sensor read and status send
        print("[CONTROLLER] Performing initial sensor read...")
        time.sleep_ms(500)
        self._readAllSensors()
        self.sendAllSensorData()
        self.sendAllStatus()
        
        print("=" * 50)
        print("[CONTROLLER] Main loop starting...")
        print(f"[CONTROLLER] Sensor read interval: {SENSOR_READ_INTERVAL_MS}ms")
        print(f"[CONTROLLER] Data send interval: {DATA_SEND_INTERVAL_MS}ms")
        print("=" * 50)
        
        while True:
            try:
                currentTime = time.ticks_ms()
                self.loopCount += 1
                
                # Heartbeat LED
                self.led.toggle()
                
                # Process any incoming commands from ESP32
                self._processCommands()
                
                # Read sensors periodically
                if time.ticks_diff(currentTime, self.lastSensorRead) >= SENSOR_READ_INTERVAL_MS:
                    print("")
                    print(f"[CONTROLLER] === Loop #{self.loopCount} - Sensor Read ===")
                    self._readAllSensors()
                    self.lastSensorRead = currentTime
                
                # Update all systems (run automatic control logic)
                self._updateSystems()
                
                # Send data to ESP32 periodically
                if time.ticks_diff(currentTime, self.lastDataSend) >= DATA_SEND_INTERVAL_MS:
                    print("")
                    print("[CONTROLLER] === Sending data to ESP32 ===")
                    self.sendAllSensorData()
                    self._logSystemStatus()
                    self.lastDataSend = currentTime
                
                # Small delay to prevent busy loop
                time.sleep_ms(100)
                
            except Exception as e:
                print(f"[CONTROLLER] ERROR in main loop: {e}")
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
        print(f"[CONTROLLER] Received command from ESP32: {cmd}")
        
        # Request commands
        if cmd == "REQ:SENSORS":
            print("[CONTROLLER] -> Responding with sensor data")
            self.sendAllSensorData()
            
        elif cmd == "REQ:STATUS":
            print("[CONTROLLER] -> Responding with system status")
            self.sendAllStatus()
        
        # Watering system commands
        elif cmd == "CMD:WATER:ON":
            print("[CONTROLLER] -> Enabling Watering System")
            self.wateringSystem.enable()
            self.uart.sendStatus("WATER", True)
            
        elif cmd == "CMD:WATER:OFF":
            print("[CONTROLLER] -> Disabling Watering System")
            self.wateringSystem.disable()
            self.uart.sendStatus("WATER", False)
        
        # Lighting system commands
        elif cmd == "CMD:LIGHT:ON":
            print("[CONTROLLER] -> Enabling Lighting System")
            self.lightingSystem.enable()
            self.uart.sendStatus("LIGHT", True)
            
        elif cmd == "CMD:LIGHT:OFF":
            print("[CONTROLLER] -> Disabling Lighting System")
            self.lightingSystem.disable()
            self.uart.sendStatus("LIGHT", False)
        
        # Air quality system commands
        elif cmd == "CMD:AIR:ON":
            print("[CONTROLLER] -> Enabling Air Quality System")
            self.airQualitySystem.enable()
            self.uart.sendStatus("AIR", True)
            
        elif cmd == "CMD:AIR:OFF":
            print("[CONTROLLER] -> Disabling Air Quality System")
            self.airQualitySystem.disable()
            self.uart.sendStatus("AIR", False)
        
        # Manual direct device controls (Options page)
        elif cmd == "CMD:LED:ON":
            print("[CONTROLLER] -> Manual LED ON")
            self.lightingSystem.light.turnOn()
            self.lightingSystem.isLightOn = True
            
        elif cmd == "CMD:LED:OFF":
            print("[CONTROLLER] -> Manual LED OFF")
            self.lightingSystem.light.turnOff()
            self.lightingSystem.isLightOn = False
            
        elif cmd == "CMD:FAN:ON":
            print("[CONTROLLER] -> Manual FAN ON")
            self.airQualitySystem.fan.turnOn()
            self.airQualitySystem.isFanOn = True
            
        elif cmd == "CMD:FAN:OFF":
            print("[CONTROLLER] -> Manual FAN OFF")
            self.airQualitySystem.fan.turnOff()
            self.airQualitySystem.isFanOn = False
            
        elif cmd == "CMD:PUMP:PULSE":
            print("[CONTROLLER] -> Manual PUMP PULSE triggered")
            self.wateringSystem.pulse()
        
        else:
            print(f"[CONTROLLER] WARNING: Unknown command: {cmd}")
    
    def _readAllSensors(self):
        """Read all sensor values (for caching)"""
        print("[CONTROLLER] Reading all sensors...")
        self.airQualitySystem.readSensor()
    
    def _updateSystems(self):
        """Run automatic control logic for all enabled systems"""
        self.wateringSystem.update()
        self.airQualitySystem.update()
        self.lightingSystem.update()
    
    def _logSystemStatus(self):
        """Log current status of all systems"""
        print("-" * 40)
        print("[STATUS] Watering: " + self.wateringSystem.getStatus())
        print("[STATUS] Air Quality: " + self.airQualitySystem.getStatus())
        print("[STATUS] Lighting: " + self.lightingSystem.getStatus())
        print("-" * 40)
    
    def sendAllSensorData(self):
        """Send all sensor readings to ESP32"""
        temp = self.airQualitySystem.getTemperature()
        humidity = self.airQualitySystem.getHumidity()
        soil = self.wateringSystem.getSoilMoisturePercent()
        water = self.wateringSystem.getWaterLevelPercent()
        
        print(f"[CONTROLLER] Sending to ESP32: Temp={temp:.1f}°C, Humidity={humidity:.1f}%, Soil={soil:.1f}%, Water={water:.1f}%")
        
        self.uart.sendSensorData("TEMP", temp)
        self.uart.sendSensorData("HUMIDITY", humidity)
        self.uart.sendSensorData("SOIL", soil)
        self.uart.sendSensorData("WATER", water)
    
    def sendAllStatus(self):
        """Send status of all systems to ESP32"""
        print(f"[CONTROLLER] Sending status to ESP32: Water={self.wateringSystem.enabled}, Light={self.lightingSystem.enabled}, Air={self.airQualitySystem.enabled}")
        
        self.uart.sendStatus("WATER", self.wateringSystem.enabled)
        self.uart.sendStatus("LIGHT", self.lightingSystem.enabled)
        self.uart.sendStatus("AIR", self.airQualitySystem.enabled)
