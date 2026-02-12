from machine import Pin
import time

# Relay control pin (change if needed)
relay = Pin(15, Pin.OUT)

# Some relay modules are ACTIVE LOW
# If yours is ACTIVE HIGH, swap 0 and 1 below

while True:
    relay.value(0)   # Relay ON
    print("Relay ON")
    time.sleep(2)

    relay.value(1)   # Relay OFF
    print("Relay OFF")
    time.sleep(2)
