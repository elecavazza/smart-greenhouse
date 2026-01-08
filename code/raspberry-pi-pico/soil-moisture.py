from machine import ADC
import time

soil = ADC(26)

# Calibrate THESE using your own measurements
AIR = 65000       # sensor in air (dry)
DRY_SOIL = 50000
MOIST_SOIL = 38000
WET_SOIL = 26000
WATER = 15000     # sensor in water

def soil_level(raw):
    if raw > AIR:
        return "BONE DRY"
    elif raw > DRY_SOIL:
        return "VERY DRY"
    elif raw > MOIST_SOIL:
        return "DRY"
    elif raw > WET_SOIL:
        return "MOIST"
    elif raw > WATER:
        return "WET"
    else:
        return "SOAKED"

def read_avg(adc, samples=10):
    return sum(adc.read_u16() for _ in range(samples)) // samples

while True:
    raw = read_avg(soil)
    voltage = raw * 3.3 / 65535
    level = soil_level(raw)

    print(f"Soil raw value: {raw}")
    print(f"Voltage: {voltage:.2f} V")
    print(f"Soil level: {level}")
    print("-----------------------")

    time.sleep(1)
