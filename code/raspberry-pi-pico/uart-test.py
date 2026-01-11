from machine import UART
import time

uart = UART(0, baudrate=115200, tx=0, rx=1)

i = 0
while True:
    uart.write(f"Hello from Pico {i}\n")
    i += 1
    time.sleep(1)