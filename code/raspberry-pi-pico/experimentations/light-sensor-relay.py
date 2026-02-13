from machine import Pin, ADC
import time

# Relay control pin (change if needed)
relay = Pin(15, Pin.OUT)

ldr = ADC(27)  # Initialize an ADC object for pin 27

# Some relay modules are ACTIVE LOW
# If yours is ACTIVE HIGH, swap 0 and 1 below

while True:
    ldr_value = ldr.read_u16()
    print(f"Light sensor reading: {ldr_value}")
    if ldr_value > 1000:
        print("Turning LED On")
        relay.value(1)
    else:
        print("Turning LED Off")
        relay.value(0) 
    time.sleep(2)
