from machine import Pin, I2C
from aht30 import AHT30
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
sensor = AHT30(i2c)

while True:
    temp, hum = sensor.read()
    print("Temperature: {:.2f} °C".format(temp))
    print("Humidity: {:.2f} %".format(hum))
    print("----------------------")
    time.sleep(2)
