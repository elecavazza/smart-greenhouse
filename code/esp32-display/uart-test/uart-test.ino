void setup() {
  Serial.begin(115200);              // USB monitor
  Serial1.begin(115200, SERIAL_8N1, 20, 21); // RX, TX
}

void loop() {
  if (Serial1.available()) {
    String s = Serial1.readStringUntil('\n');
    Serial.println(s);
  }
}