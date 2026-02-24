"""
UART Communication Module
Handles serial communication between Pico and ESP32 display
"""

from machine import UART, Pin
from config import UART_TX_PIN, UART_RX_PIN, UART_BAUDRATE


class UARTCommunication:
    """Handles UART communication with ESP32 display"""
    
    def __init__(self):
        """Initialize UART0 for ESP32 communication"""
        self.uart = UART(0, baudrate=UART_BAUDRATE, tx=Pin(UART_TX_PIN), rx=Pin(UART_RX_PIN))
    
    def send(self, message):
        """Send a message to ESP32 (adds newline terminator)"""
        self.uart.write(message + "\n")
    
    def sendSensorData(self, sensorType, value):
        """Send sensor data in format SENSOR:TYPE:VALUE"""
        self.send(f"SENSOR:{sensorType}:{value:.1f}")
    
    def sendStatus(self, system, state):
        """Send system status in format STATUS:SYSTEM:ON/OFF"""
        stateStr = "ON" if state else "OFF"
        self.send(f"STATUS:{system}:{stateStr}")
    
    def sendReady(self):
        """Send ready signal to ESP32"""
        self.send("PICO:READY")
    
    def hasData(self):
        """Check if data is available to read"""
        return self.uart.any() > 0
    
    def receive(self):
        """Read and return a line from UART (blocking until newline or timeout)"""
        if self.uart.any():
            try:
                line = self.uart.readline()
                if line:
                    return line.decode().strip()
            except Exception as e:
                print(f"UART read error: {e}")
        return None
    
    def receiveAll(self):
        """Read all available lines and return as list"""
        lines = []
        while self.uart.any():
            try:
                line = self.uart.readline()
                if line:
                    decoded = line.decode().strip()
                    if decoded:
                        lines.append(decoded)
            except Exception as e:
                print(f"UART read error: {e}")
                break
        return lines
    
    def flush(self):
        """Clear any pending data in UART buffer"""
        while self.uart.any():
            self.uart.read(1)
