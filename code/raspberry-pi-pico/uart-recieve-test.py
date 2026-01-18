from machine import UART, Pin
import time

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

print("Pico UART ready")

while True:
    # Read commands from ESP32
    if uart.any():
        line = uart.readline()
        if line:
            cmd = line.decode().strip()
            print("From ESP32:", cmd)

            if cmd == "CMD:REQ":
                # Example sensor value
                uart.write("SENSOR:TEMP:24.6\n")

    time.sleep(0.01)