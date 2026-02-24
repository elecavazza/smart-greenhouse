#define RX_P3 35
#define TX_P3 22

void setup() {
  Serial.begin(115200); // USB debug
  Serial2.begin(115200, SERIAL_8N1, RX_P3, TX_P3);

  Serial.println("ESP32 UART ready (P3)");
}

void loop() {
  // Example: send command every 2 seconds
  static unsigned long lastSend = 0;
  if (millis() - lastSend > 2000) {
    Serial2.println("CMD:REQ");
    lastSend = millis();
  }

  // Read from Pico
  while (Serial2.available()) {
    String line = Serial2.readStringUntil('\n');
    line.trim();
    if (line.length()) {
      Serial.println("From Pico: " + line);
    }
  }
}