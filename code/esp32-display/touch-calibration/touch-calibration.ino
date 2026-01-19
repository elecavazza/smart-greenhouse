/*  Touch Screen Raw Coordinate Reader
    ESP32-2432S028R (Cheap Yellow Display)
    
    INSTRUCTIONS:
    1. Upload this sketch to your ESP32
    2. Open Serial Monitor (115200 baud)
    3. Manually touch each corner of the screen:
       - TOP-LEFT corner
       - TOP-RIGHT corner
       - BOTTOM-RIGHT corner
       - BOTTOM-LEFT corner
    4. Read the Raw X and Y values from Serial Monitor
    5. Report those values to update your main sketch
*/

#include <TFT_eSPI.h>
#include <XPT2046_Touchscreen.h>

/* ---------------- TOUCH PINS ---------------- */
#define XPT2046_IRQ 36
#define XPT2046_MOSI 32
#define XPT2046_MISO 39
#define XPT2046_CLK 25
#define XPT2046_CS 33

SPIClass touchscreenSPI = SPIClass(VSPI);
XPT2046_Touchscreen touchscreen(XPT2046_CS, XPT2046_IRQ);

/* ---------------- DISPLAY ---------------- */
TFT_eSPI tft = TFT_eSPI();

/* ---------------- SETUP ---------------- */
void setup() {
  Serial.begin(115200);
  delay(2000);
  
  Serial.println("\n\n========================================");
  Serial.println("Touch Screen Raw Coordinate Reader");
  Serial.println("========================================");
  Serial.println("\nINSTRUCTIONS:");
  Serial.println("1. Touch the TOP-LEFT corner of screen");
  Serial.println("2. Touch the TOP-RIGHT corner of screen");
  Serial.println("3. Touch the BOTTOM-RIGHT corner of screen");
  Serial.println("4. Touch the BOTTOM-LEFT corner of screen");
  Serial.println("\nNote the Raw X and Y values for each corner");
  Serial.println("----------------------------------------\n");
  
  // Initialize display
  tft.init();
  tft.setRotation(1); // Landscape mode (320x240)
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_WHITE, TFT_BLACK);
  tft.setTextSize(2);
  
  // Display instructions
  tft.setCursor(10, 10);
  tft.println("Touch Calibration");
  tft.setCursor(10, 40);
  tft.println("Touch each corner:");
  tft.setCursor(10, 70);
  tft.println("1. Top-Left");
  tft.setCursor(10, 95);
  tft.println("2. Top-Right");
  tft.setCursor(10, 120);
  tft.println("3. Bottom-Right");
  tft.setCursor(10, 145);
  tft.println("4. Bottom-Left");
  tft.setCursor(10, 180);
  tft.setTextSize(1);
  tft.println("Check Serial Monitor");
  tft.println("for coordinates");
  
  // Initialize touchscreen
  touchscreenSPI.begin(XPT2046_CLK, XPT2046_MISO, XPT2046_MOSI, XPT2046_CS);
  touchscreen.begin(touchscreenSPI);
  touchscreen.setRotation(2);
  
  Serial.println("Ready! Touch the screen corners...\n");
}

/* ---------------- LOOP ---------------- */
unsigned long last_print_time = 0;
bool was_touched = false;

void loop() {
  // Check if screen is touched
  if (touchscreen.tirqTouched() && touchscreen.touched()) {
    if (!was_touched) {
      // Get raw touch coordinates
      TS_Point p = touchscreen.getPoint();
      
      // Print to Serial Monitor
      Serial.print("Touch detected! Raw X = ");
      Serial.print(p.x);
      Serial.print(", Raw Y = ");
      Serial.println(p.y);
      
      was_touched = true;
      last_print_time = millis();
    }
  } else {
    // Reset touch flag when released
    if (was_touched && (millis() - last_print_time > 200)) {
      was_touched = false;
    }
  }
  
  delay(50);
}