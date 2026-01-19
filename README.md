# smart-greenhouse

As part of my Mechatronics Project I will be creating a Smart Automated Greenhouse.  
As part of this project there will be a number of systems:  

* Watering system
  * 5v pump with relay control
  * Water level sensor
  * Reservoir
  * Shower head
  * Soil moisture sensor
* Lighting System
  * 12V Grow LED Strip with relay
* Air Quality System
  * 5V Fan with relay
  * VOC, Temperature, Humidity Sensors
* User Interface
  * Touch screen

## Programming

### CYD ESP32-2432S028

To program the CYD ESP32-2432S028 we will be using Arduino C/C++.  
To upload code to the device we use the Arduino IDE to compile it and the Micro USB connector to upload it via serial.  
To get it to work:  

* upload at a baud rate of 115200  
* target board used is the `ESP32 Dev Module`
* the external dependencies are:  `lvgl`, `TFT_eSPI`, `XPT2046_Touchscreen`
* enable erase all flash on sketch upload

### Raspberry Pi Pico

To program the Raspberry Pi Pico we will be using MicroPython.  
To upload code to the device we use the Thonny IDE and upload via the Micro USB connector.  

## Parts

### Electronics

Relays: 5v, 12, 24v etc:  
![relay](./pictures/components/relay.jpg)

5V Led Grow Strip:  
![5v led](./pictures/components/5v-grow-led.jpg)
12V Led Grow Strip:  
![12v](./pictures/components/12v-grow-led.jpg)
CO2 Sensor:  
![co2 sensor](./pictures/components/co2-sensor.jpg)

Soil Moisture Sensor:  
![soil moisture sensor](./pictures/components/soil-moisture-sensor.jpg)

Submersible Pump:  
![submersible pump](./pictures/components/submersible-pump.jpg)

Water Level Sensor:  
![water-level-sensor](./pictures/components/water-level-sensor.jpg)

Temperature and Humidity Sensor:  
![temperature-humidity-sensor](./pictures/components/temperature-humidity-sensor.jpg)

### GreenHouse/Plant

Ikea Bittergurka Pot:
![Ikea Bittergurka](./pictures/ikea/bittergurka-plant-pot-white__0748653_pe745118_s5.jpg)
![Ikea Bittergurka Dimensions](./pictures/ikea/bittergurka-plant-pot-white__1094375_pe863395_s5.jpg.avif)

[3D Model](./3d-models/bittergurka-plant-pot-white-80285787.fbx)

Ikea Akerbaer Greenhouse:
![Ikea Akerbaer](./pictures/ikea/akerbaer-greenhouse-in-outdoor-white__1176982_pe895190_s5.jpg)
![Ikea Akerbaer Dimensions](./pictures/ikea/akerbaer-greenhouse-in-outdoor-white__1357160_pe953473_s5.jpg)

[3D Model](./3d-models/akerbar-white-30537170.fbx)
