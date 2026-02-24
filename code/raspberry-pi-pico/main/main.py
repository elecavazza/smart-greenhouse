"""
Smart Greenhouse Control System
Raspberry Pi Pico W - Main Entry Point

This is the main entry point for the greenhouse controller.
It initializes all systems and runs the main control loop.

Systems:
- Watering System: Automatic pulse watering based on soil moisture
- Air Quality System: Fan control based on temperature/humidity
- Lighting System: Grow light control based on ambient light

Communication:
- UART to ESP32 display for UI and manual control
"""

from GreenhouseController import GreenhouseController


def main():
    """Main entry point"""
    print("=" * 40)
    print("Smart Greenhouse Control System")
    print("Raspberry Pi Pico W")
    print("=" * 40)
    
    # Create and run the greenhouse controller
    controller = GreenhouseController()
    controller.run()


if __name__ == "__main__":
    main()
