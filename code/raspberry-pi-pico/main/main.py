# from TemperatureAndHumiditySensor import TemperatureAndHumiditySensor
# import time


# sensor = TemperatureAndHumiditySensor(serialClockLinePinNumber = 5, serialDataLinePinNumber = 4)

# while True:
#     temperature, humidty = sensor.read()
#     print("Temperature: {:.2f} °C".format(temperature))
#     print("Humidity: {:.2f} %".format(humidty))
#     print("----------------------")
#     time.sleep(2)




# from Relay import Relay
# import time
# fan = Relay(15)

# while True:
#     fan.turnOn()
#     print("Fan ON")
#     time.sleep(5)

#     fan.turnOff()
#     print("Fan OFF")
#     time.sleep(5)


from SoilMoistureSensor import SoilMoistureSensor
soilMoistureSensor = SoilMoistureSensor(26)

moistureLevel = soilMoistureSensor.readLevel()
print("moisture level is:", moistureLevel)

dry = soilMoistureSensor.isItDry()
print("moisture level is dry?:", dry)
print("moisture level is wet?:", not dry)