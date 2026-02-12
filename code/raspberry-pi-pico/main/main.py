# from TemperatureAndHumiditySensor import TemperatureAndHumiditySensor
# import time


# sensor = TemperatureAndHumiditySensor(serialClockLinePinNumber = 1, serialDataLinePinNumber = 0)

# while True:
#     temperature, humidty = sensor.read()
#     print("Temperature: {:.2f} °C".format(temperature))
#     print("Humidity: {:.2f} %".format(humidty))
#     print("----------------------")
#     time.sleep(2)




from Relay import Relay
import time
fan = Relay(15)

while True:
    fan.turnOn()
    print("Fan ON")
    time.sleep(5)

    fan.turnOff()
    print("Fan OFF")
    time.sleep(5)