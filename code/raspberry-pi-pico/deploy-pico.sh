#!/bin/bash
#
# Smart Greenhouse - Pico Deployment Script
# Uploads all Python files to Raspberry Pi Pico W
#
# Prerequisites:
#   pip install mpremote
#
# Usage:
#   ./deploy-pico.sh           # Auto-detect Pico and upload
#   ./deploy-pico.sh /dev/tty.usbmodem1234  # Specify port
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directory containing Pico files
PICO_DIR="./main"

# Files to upload (in dependency order)
FILES=(
    "config.py"
    "Relay.py"
    "SoilMoistureSensor.py"
    "WaterLevelSensor.py"
    "TemperatureAndHumiditySensor.py"
    "LightSensor.py"
    "UARTCommunication.py"
    "WateringSystem.py"
    "AirQualitySystem.py"
    "LightingSystem.py"
    "GreenhouseController.py"
    "main.py"
)

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Smart Greenhouse - Pico Deployment${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# # Check if mpremote is installed
# if ! command -v mpremote &> /dev/null; then
#     echo -e "${RED}Error: mpremote not found${NC}"
#     echo "Install it with: pip install mpremote"
#     exit 1
# fi

# Determine the port
if [ -n "$1" ]; then
    PORT="$1"
    echo -e "${YELLOW}Using specified port: $PORT${NC}"
else
    echo -e "${YELLOW}Auto-detecting Pico...${NC}"
    # Try to find the Pico
    PORT=$(/Users/elenacavazza/Library/Python/3.9/bin/mpremote connect list 2>/dev/null | grep -i "pico\|usb" | head -1 | awk '{print $1}' || true)
    
    if [ -z "$PORT" ]; then
        echo -e "${RED}Error: Could not auto-detect Pico${NC}"
        echo "Available ports:"
        /Users/elenacavazza/Library/Python/3.9/bin/mpremote connect list
        echo ""
        echo "Usage: $0 /dev/tty.usbmodem..."
        exit 1
    fi
    echo -e "${GREEN}Found Pico at: $PORT${NC}"
fi

echo ""
echo -e "${YELLOW}Uploading files to Pico...${NC}"
echo ""

# Upload each file
for file in "${FILES[@]}"; do
    filepath="$PICO_DIR/$file"
    if [ -f "$filepath" ]; then
        echo -n "  Uploading $file... "
        /Users/elenacavazza/Library/Python/3.9/bin/mpremote connect "$PORT" cp "$filepath" ":$file"
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "  ${RED}Missing: $filepath${NC}"
    fi
done

echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Upload complete!${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo "To run the greenhouse controller:"
echo "  mpremote connect $PORT run :main.py"
echo ""
echo "Or reset the Pico to start automatically:"
echo "  mpremote connect $PORT reset"
echo ""
