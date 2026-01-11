/*  Automated Indoor Greenhouse Control System UI
    Hardware: ESP32-2432S028R (Cheap Yellow Display)
    Display: 2.8 inch 240×320 TFT with Touchscreen
*/

#include <lvgl.h>
#include <TFT_eSPI.h>
#include <XPT2046_Touchscreen.h>

// Touchscreen pins
#define XPT2046_IRQ 36
#define XPT2046_MOSI 32
#define XPT2046_MISO 39
#define XPT2046_CLK 25
#define XPT2046_CS 33

SPIClass touchscreenSPI = SPIClass(VSPI);
XPT2046_Touchscreen touchscreen(XPT2046_CS, XPT2046_IRQ);

#define SCREEN_WIDTH 240
#define SCREEN_HEIGHT 320

int x, y, z;

#define DRAW_BUF_SIZE (SCREEN_WIDTH * SCREEN_HEIGHT / 10 * (LV_COLOR_DEPTH / 8))
uint32_t draw_buf[DRAW_BUF_SIZE / 4];

// System state variables
bool pump_active = false;
bool light_active = false;
bool fan_active = false;

// Mock sensor data
float temperature = 24.5;
float humidity = 65.0;
int voc_level = 125;
int soil_moisture = 45;
int water_level = 75;

// UI Objects
lv_obj_t * tabview;
lv_obj_t * temp_label;
lv_obj_t * humidity_label;
lv_obj_t * voc_label;
lv_obj_t * soil_label;
lv_obj_t * water_label;
lv_obj_t * pump_btn;
lv_obj_t * light_btn;
lv_obj_t * fan_btn;
lv_obj_t * pump_status_led;
lv_obj_t * light_status_led;
lv_obj_t * fan_status_led;

void log_print(lv_log_level_t level, const char * buf) {
  LV_UNUSED(level);
  Serial.println(buf);
  Serial.flush();
}

void touchscreen_read(lv_indev_t * indev, lv_indev_data_t * data) {
  if(touchscreen.tirqTouched() && touchscreen.touched()) {
    TS_Point p = touchscreen.getPoint();
    x = map(p.x, 200, 3700, 1, SCREEN_WIDTH);
    y = map(p.y, 240, 3800, 1, SCREEN_HEIGHT);
    z = p.z;
    data->state = LV_INDEV_STATE_PRESSED;
    data->point.x = x;
    data->point.y = y;
  }
  else {
    data->state = LV_INDEV_STATE_RELEASED;
  }
}

// Update LED indicator color based on state
void update_led(lv_obj_t * led, bool state) {
  if (state) {
    lv_obj_set_style_bg_color(led, lv_color_hex(0x00FF00), 0); // Green
  } else {
    lv_obj_set_style_bg_color(led, lv_color_hex(0xFF0000), 0); // Red
  }
}

// Pump control callback
static void pump_event_handler(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    pump_active = !pump_active;
    update_led(pump_status_led, pump_active);
    lv_label_set_text(lv_obj_get_child(pump_btn, 0), pump_active ? "STOP" : "START");
    Serial.print("Pump: ");
    Serial.println(pump_active ? "ON" : "OFF");
  }
}

// Light control callback
static void light_event_handler(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    light_active = !light_active;
    update_led(light_status_led, light_active);
    lv_label_set_text(lv_obj_get_child(light_btn, 0), light_active ? "TURN OFF" : "LIGHTS ON");
    Serial.print("Lights: ");
    Serial.println(light_active ? "ON" : "OFF");
  }
}

// Fan control callback
static void fan_event_handler(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    fan_active = !fan_active;
    update_led(fan_status_led, fan_active);
    lv_label_set_text(lv_obj_get_child(fan_btn, 0), fan_active ? "STOP" : "START FAN");
    Serial.print("Fan: ");
    Serial.println(fan_active ? "ON" : "OFF");
  }
}

// Create Dashboard Tab
void create_dashboard_tab(lv_obj_t * parent) {
  lv_obj_set_style_pad_all(parent, 0, 0);
  
  // Title
  lv_obj_t * title = lv_label_create(parent);
  lv_label_set_text(title, "GREENHOUSE");
  lv_obj_set_style_text_font(title, &lv_font_montserrat_12, 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 2);

  // Temperature Section
  lv_obj_t * temp_container = lv_obj_create(parent);
  lv_obj_set_size(temp_container, 310, 30);
  lv_obj_align(temp_container, LV_ALIGN_TOP_LEFT, 5, 20);
  lv_obj_set_style_bg_color(temp_container, lv_color_hex(0xFF6B35), 0);
  lv_obj_set_style_pad_all(temp_container, 2, 0);
  
  lv_obj_t * temp_icon = lv_label_create(temp_container);
  lv_label_set_text(temp_icon, LV_SYMBOL_HOME);
  lv_obj_align(temp_icon, LV_ALIGN_LEFT_MID, 3, 0);
  
  temp_label = lv_label_create(temp_container);
  lv_label_set_text(temp_label, "Temp: 24.5C");
  lv_obj_align(temp_label, LV_ALIGN_CENTER, 8, 0);

  // Humidity Section
  lv_obj_t * hum_container = lv_obj_create(parent);
  lv_obj_set_size(hum_container, 310, 30);
  lv_obj_align(hum_container, LV_ALIGN_TOP_LEFT, 5, 52);
  lv_obj_set_style_bg_color(hum_container, lv_color_hex(0x004E89), 0);
  lv_obj_set_style_pad_all(hum_container, 2, 0);
  
  lv_obj_t * hum_icon = lv_label_create(hum_container);
  lv_label_set_text(hum_icon, LV_SYMBOL_EYE_OPEN);
  lv_obj_align(hum_icon, LV_ALIGN_LEFT_MID, 3, 0);
  
  humidity_label = lv_label_create(hum_container);
  lv_label_set_text(humidity_label, "Humidity: 65%");
  lv_obj_align(humidity_label, LV_ALIGN_CENTER, 8, 0);

  // VOC Section
  lv_obj_t * voc_container = lv_obj_create(parent);
  lv_obj_set_size(voc_container, 310, 30);
  lv_obj_align(voc_container, LV_ALIGN_TOP_LEFT, 5, 84);
  lv_obj_set_style_bg_color(voc_container, lv_color_hex(0x9B5094), 0);
  lv_obj_set_style_pad_all(voc_container, 2, 0);
  
  lv_obj_t * voc_icon = lv_label_create(voc_container);
  lv_label_set_text(voc_icon, LV_SYMBOL_WARNING);
  lv_obj_align(voc_icon, LV_ALIGN_LEFT_MID, 3, 0);
  
  voc_label = lv_label_create(voc_container);
  lv_label_set_text(voc_label, "VOC: 125 ppb");
  lv_obj_align(voc_label, LV_ALIGN_CENTER, 8, 0);

  // Soil Moisture Section
  lv_obj_t * soil_container = lv_obj_create(parent);
  lv_obj_set_size(soil_container, 310, 30);
  lv_obj_align(soil_container, LV_ALIGN_TOP_LEFT, 5, 116);
  lv_obj_set_style_bg_color(soil_container, lv_color_hex(0x8B4513), 0);
  lv_obj_set_style_pad_all(soil_container, 2, 0);
  
  lv_obj_t * soil_icon = lv_label_create(soil_container);
  lv_label_set_text(soil_icon, LV_SYMBOL_SETTINGS);
  lv_obj_align(soil_icon, LV_ALIGN_LEFT_MID, 3, 0);
  
  soil_label = lv_label_create(soil_container);
  lv_label_set_text(soil_label, "Soil: 45%");
  lv_obj_align(soil_label, LV_ALIGN_CENTER, 8, 0);

  // Water Level Section
  lv_obj_t * water_container = lv_obj_create(parent);
  lv_obj_set_size(water_container, 310, 30);
  lv_obj_align(water_container, LV_ALIGN_TOP_LEFT, 5, 148);
  lv_obj_set_style_bg_color(water_container, lv_color_hex(0x1982C4), 0);
  lv_obj_set_style_pad_all(water_container, 2, 0);
  
  lv_obj_t * water_icon = lv_label_create(water_container);
  lv_label_set_text(water_icon, LV_SYMBOL_BATTERY_FULL);
  lv_obj_align(water_icon, LV_ALIGN_LEFT_MID, 3, 0);
  
  water_label = lv_label_create(water_container);
  lv_label_set_text(water_label, "Water: 75%");
  lv_obj_align(water_label, LV_ALIGN_CENTER, 8, 0);
}

// Create Controls Tab
void create_controls_tab(lv_obj_t * parent) {
  lv_obj_set_style_pad_all(parent, 0, 0);
  
  // Title
  lv_obj_t * title = lv_label_create(parent);
  lv_label_set_text(title, "CONTROLS");
  lv_obj_set_style_text_font(title, &lv_font_montserrat_12, 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 2);

  // Pump Control
  lv_obj_t * pump_container = lv_obj_create(parent);
  lv_obj_set_size(pump_container, 310, 52);
  lv_obj_align(pump_container, LV_ALIGN_TOP_LEFT, 5, 20);
  
  lv_obj_set_style_pad_all(pump_container, 3, 0);
  
  lv_obj_t * pump_label = lv_label_create(pump_container);
  lv_label_set_text(pump_label, "Water Pump (5V)");
  lv_obj_set_style_text_font(pump_label, &lv_font_montserrat_10, 0);
  lv_obj_align(pump_label, LV_ALIGN_TOP_LEFT, 3, 2);
  
  pump_btn = lv_button_create(pump_container);
  lv_obj_set_size(pump_btn, 90, 25);
  lv_obj_align(pump_btn, LV_ALIGN_BOTTOM_LEFT, 3, -3);
  lv_obj_add_event_cb(pump_btn, pump_event_handler, LV_EVENT_CLICKED, NULL);
  
  lv_obj_t * pump_btn_label = lv_label_create(pump_btn);
  lv_label_set_text(pump_btn_label, "START");
  lv_obj_set_style_text_font(pump_btn_label, &lv_font_montserrat_10, 0);
  lv_obj_center(pump_btn_label);
  
  pump_status_led = lv_obj_create(pump_container);
  lv_obj_set_size(pump_status_led, 16, 16);
  lv_obj_align(pump_status_led, LV_ALIGN_BOTTOM_RIGHT, -3, -7);
  lv_obj_set_style_radius(pump_status_led, LV_RADIUS_CIRCLE, 0);
  lv_obj_set_style_bg_color(pump_status_led, lv_color_hex(0xFF0000), 0);

  // Light Control
  lv_obj_t * light_container = lv_obj_create(parent);
  lv_obj_set_size(light_container, 310, 52);
  lv_obj_align(light_container, LV_ALIGN_TOP_LEFT, 5, 75);
  
  lv_obj_set_style_pad_all(light_container, 3, 0);
  
  lv_obj_t * light_label = lv_label_create(light_container);
  lv_label_set_text(light_label, "Grow Lights (12V)");
  lv_obj_set_style_text_font(light_label, &lv_font_montserrat_10, 0);
  lv_obj_align(light_label, LV_ALIGN_TOP_LEFT, 3, 2);
  
  light_btn = lv_button_create(light_container);
  lv_obj_set_size(light_btn, 90, 25);
  lv_obj_align(light_btn, LV_ALIGN_BOTTOM_LEFT, 3, -3);
  lv_obj_add_event_cb(light_btn, light_event_handler, LV_EVENT_CLICKED, NULL);
  
  lv_obj_t * light_btn_label = lv_label_create(light_btn);
  lv_label_set_text(light_btn_label, "LIGHTS ON");
  lv_obj_set_style_text_font(light_btn_label, &lv_font_montserrat_10, 0);
  lv_obj_center(light_btn_label);
  
  light_status_led = lv_obj_create(light_container);
  lv_obj_set_size(light_status_led, 16, 16);
  lv_obj_align(light_status_led, LV_ALIGN_BOTTOM_RIGHT, -3, -7);
  lv_obj_set_style_radius(light_status_led, LV_RADIUS_CIRCLE, 0);
  lv_obj_set_style_bg_color(light_status_led, lv_color_hex(0xFF0000), 0);

  // Fan Control
  lv_obj_t * fan_container = lv_obj_create(parent);
  lv_obj_set_size(fan_container, 310, 52);
  lv_obj_align(fan_container, LV_ALIGN_TOP_LEFT, 5, 130);
  
  lv_obj_set_style_pad_all(fan_container, 3, 0);
  
  lv_obj_t * fan_label = lv_label_create(fan_container);
  lv_label_set_text(fan_label, "Ventilation Fan (5V)");
  lv_obj_set_style_text_font(fan_label, &lv_font_montserrat_10, 0);
  lv_obj_align(fan_label, LV_ALIGN_TOP_LEFT, 3, 2);
  
  fan_btn = lv_button_create(fan_container);
  lv_obj_set_size(fan_btn, 90, 25);
  lv_obj_align(fan_btn, LV_ALIGN_BOTTOM_LEFT, 3, -3);
  lv_obj_add_event_cb(fan_btn, fan_event_handler, LV_EVENT_CLICKED, NULL);
  
  lv_obj_t * fan_btn_label = lv_label_create(fan_btn);
  lv_label_set_text(fan_btn_label, "START FAN");
  lv_obj_set_style_text_font(fan_btn_label, &lv_font_montserrat_10, 0);
  lv_obj_center(fan_btn_label);
  
  fan_status_led = lv_obj_create(fan_container);
  lv_obj_set_size(fan_status_led, 16, 16);
  lv_obj_align(fan_status_led, LV_ALIGN_BOTTOM_RIGHT, -3, -7);
  lv_obj_set_style_radius(fan_status_led, LV_RADIUS_CIRCLE, 0);
  lv_obj_set_style_bg_color(fan_status_led, lv_color_hex(0xFF0000), 0);
}

void lv_create_main_gui(void) {
  // Create tabview
  tabview = lv_tabview_create(lv_screen_active());
  lv_obj_set_size(tabview, SCREEN_WIDTH, SCREEN_HEIGHT);
  lv_tabview_set_tab_bar_size(tabview, 25);
  
  // Add tabs
  lv_obj_t * tab_dashboard = lv_tabview_add_tab(tabview, "Dashboard");
  lv_obj_t * tab_controls = lv_tabview_add_tab(tabview, "Controls");
  
  // Remove scrolling from tabs
  lv_obj_remove_flag(tab_dashboard, LV_OBJ_FLAG_SCROLLABLE);
  lv_obj_remove_flag(tab_controls, LV_OBJ_FLAG_SCROLLABLE);
  
  // Create content for each tab
  create_dashboard_tab(tab_dashboard);
  create_controls_tab(tab_controls);
}

void update_sensor_displays() {
  // Simulate sensor value changes (mock data)
  static unsigned long last_update = 0;
  if (millis() - last_update > 2000) {
    last_update = millis();
    
    // Add small random variations
    temperature += (random(-10, 11) / 10.0);
    humidity += (random(-20, 21) / 10.0);
    voc_level += random(-5, 6);
    soil_moisture += random(-2, 3);
    water_level -= pump_active ? 1 : 0;
    
    // Keep values in reasonable ranges
    temperature = constrain(temperature, 20.0, 30.0);
    humidity = constrain(humidity, 50.0, 80.0);
    voc_level = constrain(voc_level, 100, 200);
    soil_moisture = constrain(soil_moisture, 30, 70);
    water_level = constrain(water_level, 0, 100);
    
    // Update labels
    char buf[32];
    sprintf(buf, "Temp: %.1fC", temperature);
    lv_label_set_text(temp_label, buf);
    
    sprintf(buf, "Humidity: %.0f%%", humidity);
    lv_label_set_text(humidity_label, buf);
    
    sprintf(buf, "VOC: %d ppb", voc_level);
    lv_label_set_text(voc_label, buf);
    
    sprintf(buf, "Soil: %d%%", soil_moisture);
    lv_label_set_text(soil_label, buf);
    
    sprintf(buf, "Water: %d%%", water_level);
    lv_label_set_text(water_label, buf);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Greenhouse Control System Starting...");
  
  // Start LVGL
  lv_init();
  lv_log_register_print_cb(log_print);

  // Start touchscreen
  touchscreenSPI.begin(XPT2046_CLK, XPT2046_MISO, XPT2046_MOSI, XPT2046_CS);
  touchscreen.begin(touchscreenSPI);
  touchscreen.setRotation(2);

  // Create display
  lv_display_t * disp;
  disp = lv_tft_espi_create(SCREEN_WIDTH, SCREEN_HEIGHT, draw_buf, sizeof(draw_buf));
  lv_display_set_rotation(disp, LV_DISPLAY_ROTATION_270);
    
  // Initialize input device
  lv_indev_t * indev = lv_indev_create();
  lv_indev_set_type(indev, LV_INDEV_TYPE_POINTER);
  lv_indev_set_read_cb(indev, touchscreen_read);

  // Create GUI
  lv_create_main_gui();
  
  Serial.println("System Ready!");
}

void loop() {
  lv_task_handler();
  lv_tick_inc(5);
  update_sensor_displays();
  delay(5);
}