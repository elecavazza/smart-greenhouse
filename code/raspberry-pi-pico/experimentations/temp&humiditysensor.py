from machine import Pin, I2C
import time
import bme280

# Initialize I2C on SDA=4, SCL=5
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)

# Scan for devices
print("Scanning I2C bus...")
print(i2c.scan())

# Initialize sensor
sensor = bme280.BME280(i2c=i2c)

while True:
    temp, pressure, humidity = sensor.read_compensated_data()
    
    temperature_c = temp / 100
    humidity_percent = humidity / 1024

    print("Temperature: {:.2f} °C".format(temperature_c))
    print("Humidity: {:.2f} %".format(humidity_percent))
    print("-----------------------")

    time.sleep(2)