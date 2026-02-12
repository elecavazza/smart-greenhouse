"""
Smart Greenhouse Control System - Raspberry Pi Pico W (Mock Version)
Simple mock implementation for testing ESP32 communication
Generates fake sensor data and responds to control commands
"""

from machine import UART, Pin
import time
import random

# UART Communication with ESP32
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# LED for status indication
led = Pin("LED", Pin.OUT)

# Mock system state
class MockGreenhouseState:
    def __init__(self):
        # Mock sensor readings (will vary over time)
        self.temperature = 24.5
        self.humidity = 65.0
        self.soil_moisture = 45.0
        self.water_level = 75.0
        
        # Control states
        self.water_pump_active = False
        self.grow_light_active = False
        self.air_fan_active = False
        
        # Timing
        self.last_sensor_update = 0
        self.last_data_send = 0

state = MockGreenhouseState()

def update_mock_sensors():
    """Generate realistic mock sensor data that changes over time"""
    # Temperature varies slightly (22-26°C)
    state.temperature += random.uniform(-0.2, 0.2)
    state.temperature = max(22.0, min(26.0, state.temperature))
    
    # Humidity varies (60-70%)
    state.humidity += random.uniform(-1.0, 1.0)
    state.humidity = max(60.0, min(70.0, state.humidity))
    
    # Soil moisture decreases over time, increases when watering
    if state.water_pump_active:
        state.soil_moisture += 2.0  # Increase when watering
    else:
        state.soil_moisture -= 0.1  # Slowly decrease over time
    state.soil_moisture = max(0.0, min(100.0, state.soil_moisture))
    
    # Water level decreases when watering
    if state.water_pump_active:
        state.water_level -= 0.5
    else:
        state.water_level += 0.1  # Slowly refill
    state.water_level = max(0.0, min(100.0, state.water_level))
    
    state.last_sensor_update = time.ticks_ms()

def control_water_pump(active):
    """Mock control of water pump"""
    state.water_pump_active = active
    send_status_update("WATER", "ON" if active else "OFF")
    print(f"Mock Water pump: {'ON' if active else 'OFF'}")

def control_grow_light(active):
    """Mock control of grow light"""
    state.grow_light_active = active
    send_status_update("LIGHT", "ON" if active else "OFF")
    print(f"Mock Grow light: {'ON' if active else 'OFF'}")

def control_air_fan(active):
    """Mock control of air circulation fan"""
    state.air_fan_active = active
    send_status_update("AIR", "ON" if active else "OFF")
    print(f"Mock Air fan: {'ON' if active else 'OFF'}")

def send_sensor_data():
    """Send mock sensor data to ESP32"""
    uart.write(f"SENSOR:TEMP:{state.temperature:.1f}\n")
    uart.write(f"SENSOR:HUMIDITY:{state.humidity:.1f}\n")
    uart.write(f"SENSOR:SOIL:{state.soil_moisture:.1f}\n")
    uart.write(f"SENSOR:WATER:{state.water_level:.1f}\n")
    print(f"Sent sensors - T:{state.temperature:.1f}°C H:{state.humidity:.1f}% S:{state.soil_moisture:.1f}% W:{state.water_level:.1f}%")

def send_status_update(system, status):
    """Send status update to ESP32"""
    uart.write(f"STATUS:{system}:{status}\n")

def send_all_status():
    """Send current status of all systems"""
    send_status_update("WATER", "ON" if state.water_pump_active else "OFF")
    send_status_update("LIGHT", "ON" if state.grow_light_active else "OFF")
    send_status_update("AIR", "ON" if state.air_fan_active else "OFF")

def process_uart_commands():
    """Process commands from ESP32"""
    if uart.any():
        try:
            line = uart.readline()
            if line:
                cmd = line.decode().strip()
                print(f"Received: {cmd}")
                
                # Request commands
                if cmd == "REQ:SENSORS":
                    send_sensor_data()
                elif cmd == "REQ:STATUS":
                    send_all_status()
                
                # Control commands: CMD:SYSTEM:ACTION
                elif cmd.startswith("CMD:"):
                    parts = cmd.split(":")
                    if len(parts) == 3:
                        system = parts[1]
                        action = parts[2]
                        
                        if system == "WATER":
                            control_water_pump(action == "ON")
                        elif system == "LIGHT":
                            control_grow_light(action == "ON")
                        elif system == "AIR":
                            control_air_fan(action == "ON")
                
        except Exception as e:
            print(f"UART error: {e}")

def main():
    """Main mock system loop"""
    print("=== Mock Smart Greenhouse System ===")
    print("Pico W Mock - ESP32 Communication Test")
    
    # Boot LED pattern
    for _ in range(3):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)
    
    print("Mock system ready - listening for ESP32...")
    uart.write("PICO:READY\n")
    
    # Send initial sensor data
    time.sleep(1)
    send_sensor_data()
    send_all_status()
    
    # Main loop
    while True:
        try:
            # Handle UART communication
            process_uart_commands()
            
            # Update mock sensors every 2 seconds
            if time.ticks_diff(time.ticks_ms(), state.last_sensor_update) > 2000:
                led.on()
                update_mock_sensors()
                led.off()
            
            # Send sensor data every 5 seconds
            if time.ticks_diff(time.ticks_ms(), state.last_data_send) > 5000:
                send_sensor_data()
                state.last_data_send = time.ticks_ms()
            
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Main loop error: {e}")
            led.on()
            time.sleep(0.5)
            led.off()
            time.sleep(0.5)

if __name__ == "__main__":
    main()
