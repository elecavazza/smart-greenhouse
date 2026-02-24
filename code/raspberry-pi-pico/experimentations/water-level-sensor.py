from machine import ADC, Pin
import time

# GP26 is ADC0
water_sensor = ADC(28)

# Pico reference voltage
VREF = 3.3
ADC_MAX = 65535  # 16-bit ADC in MicroPython

while True:
    raw = water_sensor.read_u16()
    voltage = (raw / ADC_MAX) * VREF

    print("Raw ADC:", raw, "Voltage:", round(voltage, 2), "V")

    # Simple thresholds (adjust these!)
    if raw < 15000:
        level = "DRY"
    elif raw < 31000:
        level = "HALF"
    else:
        level = "FULL"

    print("Water level:", level)
    print("----------------------")

    time.sleep(1)
