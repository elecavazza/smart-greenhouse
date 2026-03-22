"""
Smart Greenhouse Configuration
Pin assignments and threshold constants
"""

# ============== PIN ASSIGNMENTS ==============

# Analog Sensors (ADC pins)
SOIL_MOISTURE_PIN = 26      # GP26 Capacitive soil sensor
WATER_LEVEL_PIN = 28        # GP28 Reservoir water level
LIGHT_SENSOR_PIN = 27       # GP27 Light dependent resistor

# I2C Temperature/Humidity Sensor (AHT21/30)
TEMP_HUMIDITY_SCL = 5       # GP5 - I2C clock
TEMP_HUMIDITY_SDA = 4       # GP4 - I2C data

# Relay Outputs (Active LOW)
PUMP_RELAY_PIN = 14         # GP15 - Water pump relay
FAN_RELAY_PIN = 15          # GP14 - Ventilation fan relay
LIGHT_RELAY_PIN = 10        # GP10 - Grow light relay

# UART Communication with ESP32
UART_TX_PIN = 0             # GP0 - UART0 TX
UART_RX_PIN = 1             # GP1 - UART0 RX
UART_BAUDRATE = 115200

# ============== SENSOR THRESHOLDS ==============

# Soil Moisture (Raw ADC values - higher = drier)
# Calibration: AIR ~65000, WATER ~15000
SOIL_DRY_THRESHOLD = 40000  # Above this = soil is dry, needs water

# Water Level (Raw ADC values - higher = more water)
WATER_LOW_THRESHOLD = 15000 # Below this = reservoir is empty

# Temperature (Celsius)
TEMP_HIGH_THRESHOLD = 23.0  # Above this = too hot, turn on fan
TEMP_LOW_THRESHOLD = 18.0   # Below this = too cold, turn off fan to preserve heat

# Humidity (Percentage)
HUMIDITY_HIGH_THRESHOLD = 80.0  # Above this = too humid, turn on fan
HUMIDITY_LOW_THRESHOLD = 40.0   # Below this = too dry, turn on fan to circulate

# Light (Raw ADC values - higher = brighter)
LIGHT_LOW_THRESHOLD = 1000  # Below this = too dark, turn on grow light

# ============== TIMING ==============

# Main loop intervals (milliseconds)
SENSOR_READ_INTERVAL_MS = 2000   # Read sensors every 2 seconds
DATA_SEND_INTERVAL_MS = 5000     # Send data to ESP32 every 5 seconds

# Watering System - Pulse watering to prevent overwatering
PUMP_PULSE_MS = 500              # Duration of each pump burst (500ms)
PUMP_COOLDOWN_MS = 30000         # Minimum time between pulses (30 seconds)

# ============== ADC CALIBRATION ==============

# For converting raw ADC to percentage
ADC_MAX = 65535  # 16-bit ADC maximum value

# Soil moisture calibration (inverted - lower raw = wetter)
SOIL_AIR_VALUE = 65000    # Sensor in air (0% moisture)
SOIL_WATER_VALUE = 15000  # Sensor in water (100% moisture)

# Water level calibration
WATER_EMPTY_VALUE = 10000  # Empty reservoir (0%)
WATER_FULL_VALUE = 50000   # Full reservoir (100%)

# Light sensor calibration
LIGHT_DARK_VALUE = 500     # Complete darkness (0%)
LIGHT_BRIGHT_VALUE = 50000 # Bright light (100%)
