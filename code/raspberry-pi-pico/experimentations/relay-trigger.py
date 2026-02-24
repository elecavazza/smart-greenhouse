from machine import Pin
import time

# Relay control pin (change if needed)
pinNumber = 15
relay = Pin(pinNumber, Pin.OUT)

# Some relay modules are ACTIVE LOW
# If yours is ACTIVE HIGH, swap 0 and 1 below

while True:
    relay.value(0)   # Relay ON
    print("Relay ON: pin: ", pinNumber)
    time.sleep(5)

    relay.value(1)   # Relay OFF
    print("Relay OFF: pin: ", pinNumber)
    time.sleep(5)
