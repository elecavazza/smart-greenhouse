from machine import Pin

class Relay:
    def __init__(self, pinNumber):
        self.pin = Pin(pinNumber, Pin.OUT)
    def turnOn(self):
        self.pin.value(0)
    def turnOff(self):
        self.pin.value(1)