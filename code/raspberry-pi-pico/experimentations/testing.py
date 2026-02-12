from machine import Pin, I2C
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

while True:
    print("Scan:", i2c.scan())
    time.sleep(2)
