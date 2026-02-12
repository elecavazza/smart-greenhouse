from TemperatureAndHumiditySensor import TemperatureAndHumiditySensor
import time


sensor = TemperatureAndHumiditySensor(serialClockLinePinNumber = 1, serialDataLinePinNumber = 0)

while True:
    temperature, humidty = sensor.read()
    print("Temperature: {:.2f} °C".format(temperature))
    print("Humidity: {:.2f} %".format(humidty))
    print("----------------------")
    time.sleep(2)
