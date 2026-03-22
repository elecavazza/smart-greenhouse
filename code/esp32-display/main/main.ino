/*  Smart Greenhouse Control System with UART Communication
    ESP32-2432S028R (Cheap Yellow Display) + Raspberry Pi Pico W
    
    ESP32 handles: UI Display, Touch Input, UART Communication
    Pico handles: Sensors, Actuators, Control Logic
*/

#include <lvgl.h>
#include <TFT_eSPI.h>
#include <XPT2046_Touchscreen.h>

// UART Communication pins (P3 connector)
#define RX_P3 35
#define TX_P3 22

// Touchscreen pins
#define XPT2046_IRQ 36   // T_IRQ
#define XPT2046_MOSI 32  // T_DIN
#define XPT2046_MISO 39  // T_OUT
#define XPT2046_CLK 25   // T_CLK
#define XPT2046_CS 33    // T_CS

SPIClass touchscreenSPI = SPIClass(VSPI);
XPT2046_Touchscreen touchscreen(XPT2046_CS, XPT2046_IRQ);

#define SCREEN_WIDTH 240
#define SCREEN_HEIGHT 320
// After 270° rotation, logical dimensions are swapped
#define ROTATED_WIDTH 320
#define ROTATED_HEIGHT 240

#define DRAW_BUF_SIZE (SCREEN_WIDTH * SCREEN_HEIGHT / 10 * (LV_COLOR_DEPTH / 8))
uint32_t draw_buf[DRAW_BUF_SIZE / 4];

/* ---------------- SYSTEM STATE ---------------- */
struct SensorData {
  float temperature = 0.0;
  float humidity = 0.0;
  float soil_moisture = 0.0;
  float water_level = 0.0;
  unsigned long last_update = 0;
} sensors;

struct SystemState {
  bool watering_active = false;
  bool lighting_active = false;
  bool air_active = false;
} controls;

/* ---------------- UI ELEMENTS ---------------- */
lv_obj_t *tabview;
lv_obj_t *water_btn, *light_btn, *air_btn;
lv_obj_t *water_led, *light_led, *air_led;
lv_obj_t *temp_label, *humidity_label, *soil_label, *water_label;

/* ---------------- UART COMMUNICATION ---------------- */
void sendCommand(const char* command) {
  Serial2.println(command);
  Serial.println("Sent to Pico: " + String(command));
}

void processIncomingData() {
  while (Serial2.available()) {
    String line = Serial2.readStringUntil('\n');
    line.trim();
    if (line.length() > 0) {
      Serial.println("From Pico: " + line);
      
      // Parse sensor data: SENSOR:TYPE:VALUE
    if (line.startsWith("SENSOR:")) {
      // SENSOR:TEMP:24.5
      int p1 = line.indexOf(':');
      int p2 = line.indexOf(':', p1 + 1);

      if (p1 > 0 && p2 > 0) {
        String sensor_type = line.substring(p1 + 1, p2);
        float value = line.substring(p2 + 1).toFloat();

        if (sensor_type == "TEMP") {
          sensors.temperature = value;
        } else if (sensor_type == "HUMIDITY") {
          sensors.humidity = value;
        } else if (sensor_type == "SOIL") {
          sensors.soil_moisture = value;
        } else if (sensor_type == "WATER") {
          sensors.water_level = value;
        }

        sensors.last_update = millis();
        updateDashboard();
      }
    }
      
      // Parse status updates: STATUS:SYSTEM:STATE
      else if (line.startsWith("STATUS:")) {
        int first_colon = line.indexOf(':', 7);
        int second_colon = line.indexOf(':', first_colon + 1);
        
        if (first_colon > 0 && second_colon > 0) {
          String system = line.substring(7, first_colon);
          String state = line.substring(second_colon + 1);
          
          if (system == "WATER") {
            controls.watering_active = (state == "ON");
            updateControlLED(water_led, water_btn, controls.watering_active);
          } else if (system == "LIGHT") {
            controls.lighting_active = (state == "ON");
            updateControlLED(light_led, light_btn, controls.lighting_active);
          } else if (system == "AIR") {
            controls.air_active = (state == "ON");
            updateControlLED(air_led, air_btn, controls.air_active);
          }
        }
      }
    }
  }
}

void requestSensorData() {
  static unsigned long last_request = 0;
  if (millis() - last_request > 5000) { // Request every 5 seconds
    sendCommand("REQ:SENSORS");
    last_request = millis();
  }
}

/* ---------------- UI FUNCTIONS ---------------- */
void log_print(lv_log_level_t level, const char * buf) {
  LV_UNUSED(level);
  Serial.println(buf);
  Serial.flush();
}

void touchscreen_read(lv_indev_t * indev, lv_indev_data_t * data) {
  if(touchscreen.tirqTouched() && touchscreen.touched()) {
    TS_Point p = touchscreen.getPoint();
    int x = map(p.x, 200, 3700, 1, SCREEN_WIDTH);
    int y = map(p.y, 240, 3800, 1, SCREEN_HEIGHT);

    data->state = LV_INDEV_STATE_PRESSED;
    data->point.x = x;
    data->point.y = y;

    Serial.print("Touch: X=");
    Serial.print(x);
    Serial.print(" Y=");
    Serial.println(y);
  } else {
    data->state = LV_INDEV_STATE_RELEASED;
  }
}

void set_led(lv_obj_t *led, bool on) {
  lv_obj_set_style_bg_color(
    led, on ? lv_color_hex(0x00FF00) : lv_color_hex(0xFF0000), 0
  );
}

void updateControlLED(lv_obj_t *led, lv_obj_t *btn, bool active) {
  set_led(led, active);
  lv_label_set_text(lv_obj_get_child(btn, 0), active ? "Turn Off" : "Turn On");
}

/* ---------------- CONTROL CALLBACKS ---------------- */
static void water_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    controls.watering_active = !controls.watering_active;
    sendCommand(controls.watering_active ? "CMD:WATER:ON" : "CMD:WATER:OFF");
    updateControlLED(water_led, water_btn, controls.watering_active);
    LV_LOG_USER("Watering System %s", controls.watering_active ? "ON" : "OFF");
  }
}

static void light_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    controls.lighting_active = !controls.lighting_active;
    sendCommand(controls.lighting_active ? "CMD:LIGHT:ON" : "CMD:LIGHT:OFF");
    updateControlLED(light_led, light_btn, controls.lighting_active);
    LV_LOG_USER("Lighting System %s", controls.lighting_active ? "ON" : "OFF");
  }
}

static void air_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    controls.air_active = !controls.air_active;
    sendCommand(controls.air_active ? "CMD:AIR:ON" : "CMD:AIR:OFF");
    updateControlLED(air_led, air_btn, controls.air_active);
    LV_LOG_USER("Air Quality System %s", controls.air_active ? "ON" : "OFF");
  }
}

/* ---------------- DASHBOARD FUNCTIONS ---------------- */
void dashboard_row(lv_obj_t *parent, int y, const char *label, const char *value, 
                   lv_color_t indicator_color, lv_obj_t **value_label) {
  lv_obj_t *row = lv_obj_create(parent);
  lv_obj_set_width(row, lv_pct(100));
  lv_obj_set_height(row, 40);
  lv_obj_set_pos(row, 0, y);
  lv_obj_set_style_pad_all(row, 6, 0);
  lv_obj_set_style_bg_color(row, lv_color_hex(0xF0F0F0), 0);
  lv_obj_set_style_border_width(row, 1, 0);
  lv_obj_set_style_border_color(row, lv_color_hex(0xDDDDDD), 0);
  lv_obj_remove_flag(row, LV_OBJ_FLAG_SCROLLABLE);
  lv_obj_clear_flag(row, LV_OBJ_FLAG_GESTURE_BUBBLE);

  // Label on the left
  lv_obj_t *lbl = lv_label_create(row);
  lv_label_set_text(lbl, label);
  lv_obj_set_style_text_color(lbl, lv_color_hex(0x333333), 0);
  lv_obj_align(lbl, LV_ALIGN_LEFT_MID, 8, 0);

  // Value on the right - store reference for updates
  *value_label = lv_label_create(row);
  lv_label_set_text(*value_label, value);
  lv_obj_set_style_text_color(*value_label, lv_color_hex(0x000000), 0);
  lv_obj_set_style_text_font(*value_label, &lv_font_montserrat_14, 0);
  lv_obj_align(*value_label, LV_ALIGN_RIGHT_MID, -30, 0);

  // Color indicator circle
  lv_obj_t *indicator = lv_obj_create(row);
  lv_obj_set_size(indicator, 16, 16);
  lv_obj_align(indicator, LV_ALIGN_RIGHT_MID, -6, 0);
  lv_obj_set_style_radius(indicator, LV_RADIUS_CIRCLE, 0);
  lv_obj_set_style_bg_color(indicator, indicator_color, 0);
  lv_obj_set_style_border_width(indicator, 0, 0);
}

void create_dashboard(lv_obj_t *parent) {
  dashboard_row(parent, 15,  "Temperature", "--°C", lv_color_hex(0xFF6B35), &temp_label);
  dashboard_row(parent, 65,  "Humidity", "--%", lv_color_hex(0x4D96FF), &humidity_label);
  dashboard_row(parent, 115, "Soil Moisture", "--%", lv_color_hex(0x8D6E63), &soil_label);
  dashboard_row(parent, 165, "Water Level", "--%", lv_color_hex(0x1E88E5), &water_label);
}

void updateDashboard() {
  char buffer[16];
  
  snprintf(buffer, sizeof(buffer), "%.1f°C", sensors.temperature);
  lv_label_set_text(temp_label, buffer);
  
  snprintf(buffer, sizeof(buffer), "%.0f%%", sensors.humidity);
  lv_label_set_text(humidity_label, buffer);
  
  snprintf(buffer, sizeof(buffer), "%.0f%%", sensors.soil_moisture);
  lv_label_set_text(soil_label, buffer);
  
  snprintf(buffer, sizeof(buffer), "%.0f%%", sensors.water_level);
  lv_label_set_text(water_label, buffer);
}

/* ---------------- CONTROL ROW FUNCTIONS ---------------- */
void control_row(lv_obj_t *parent, int y, const char *name,
                 lv_event_cb_t cb, lv_obj_t **btn, lv_obj_t **led) {

  lv_obj_t *row = lv_obj_create(parent);
  lv_obj_set_width(row, lv_pct(100));
  lv_obj_set_height(row, 36);
  lv_obj_set_pos(row, 0, y);
  lv_obj_set_style_pad_all(row, 4, 0);
  lv_obj_remove_flag(row, LV_OBJ_FLAG_SCROLLABLE);
  lv_obj_clear_flag(row, LV_OBJ_FLAG_GESTURE_BUBBLE);

  lv_obj_t *lbl = lv_label_create(row);
  lv_label_set_text(lbl, name);
  lv_obj_align(lbl, LV_ALIGN_LEFT_MID, 4, 0);

  *btn = lv_button_create(row);
  lv_obj_set_size(*btn, 70, 26);
  lv_obj_align(*btn, LV_ALIGN_RIGHT_MID, -30, 0);
  lv_obj_add_event_cb(*btn, cb, LV_EVENT_CLICKED, NULL);
  lv_obj_clear_flag(*btn, LV_OBJ_FLAG_GESTURE_BUBBLE);

  lv_obj_t *btxt = lv_label_create(*btn);
  lv_label_set_text(btxt, "Turn On");
  lv_obj_center(btxt);

  *led = lv_obj_create(row);
  lv_obj_set_size(*led, 14, 14);
  lv_obj_align(*led, LV_ALIGN_RIGHT_MID, -6, 0);
  lv_obj_set_style_radius(*led, LV_RADIUS_CIRCLE, 0);
  set_led(*led, false);
}

void create_controls(lv_obj_t *parent) {
  control_row(parent, 20,  "Watering System", water_cb, &water_btn, &water_led);
  control_row(parent, 70,  "Lighting System", light_cb, &light_btn, &light_led);
  control_row(parent, 120, "Air Quality System", air_cb, &air_btn, &air_led);
}

/* ---------------- GUI SETUP ---------------- */
void create_gui() {
  tabview = lv_tabview_create(lv_screen_active());
  lv_obj_set_size(tabview, ROTATED_WIDTH, ROTATED_HEIGHT);
  lv_tabview_set_tab_bar_size(tabview, 26);

  lv_obj_t *dash = lv_tabview_add_tab(tabview, "Dashboard");
  lv_obj_t *ctrl = lv_tabview_add_tab(tabview, "Controls");

  lv_obj_set_style_pad_top(dash, 8, 0);
  lv_obj_set_style_pad_top(ctrl, 8, 0);

  create_dashboard(dash);
  create_controls(ctrl);
}

/* ---------------- MAIN SETUP AND LOOP ---------------- */
void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RX_P3, TX_P3); // UART to Pico
  
  Serial.println("Smart Greenhouse Control System Starting...");
  Serial.println("ESP32 Display + Pico Communication");
  
  lv_init();
  lv_log_register_print_cb(log_print);

  // Initialize touchscreen
  touchscreenSPI.begin(XPT2046_CLK, XPT2046_MISO, XPT2046_MOSI, XPT2046_CS);
  touchscreen.begin(touchscreenSPI);
  touchscreen.setRotation(2);

  // Initialize display
  lv_display_t *disp = lv_tft_espi_create(SCREEN_WIDTH, SCREEN_HEIGHT, draw_buf, sizeof(draw_buf));
  lv_display_set_rotation(disp, LV_DISPLAY_ROTATION_270);

  // Initialize input device
  lv_indev_t *indev = lv_indev_create();
  lv_indev_set_type(indev, LV_INDEV_TYPE_POINTER);
  lv_indev_set_read_cb(indev, touchscreen_read);

  // Create GUI
  create_gui();
  
  // Request initial sensor data
  delay(1000);
  sendCommand("REQ:SENSORS");
  sendCommand("REQ:STATUS");
  
  Serial.println("System ready!");
}

void loop() {
  static uint32_t last_tick = 0;
  uint32_t now = millis();

  lv_tick_inc(now - last_tick);
  last_tick = now;

  lv_task_handler();

  processIncomingData();
  requestSensorData();

  delay(2);
}
