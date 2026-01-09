from machine import ADC, Pin
import time

relay = Pin(15, Pin.OUT)
relay.value(1)

# GP26 is ADC0
water_sensor = ADC(26)

# Pico reference voltage
VREF = 3.3
ADC_MAX = 65535  # 16-bit ADC in MicroPython

while True:
    
    raw = water_sensor.read_u16()
    voltage = (raw / ADC_MAX) * VREF

    print("Raw ADC:", raw, "Voltage:", round(voltage, 2), "V")

    # Simple thresholds
    if raw < 15000:
        print("Not enough water")
        relay.value(1)
    else: 
        print("Enough water")
        print("Turn on pump")
        relay.value(0)   # Relay ON
        print("Relay ON")
        time.sleep(0.5)

        relay.value(1)   # Relay OFF
        print("Relay OFF")
    time.sleep(1)    # OFF time unchanged
