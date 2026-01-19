/*  Automated Indoor Greenhouse Control System UI
    ESP32-2432S028R (Cheap Yellow Display)
*/

#include <lvgl.h>
#include <TFT_eSPI.h>
#include <XPT2046_Touchscreen.h>

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

/* ---------------- STATES ---------------- */
bool watering_active = false;
bool lighting_active = false;
bool air_active      = false;

/* ---------------- UI ---------------- */
lv_obj_t *tabview;
lv_obj_t *water_btn, *light_btn, *air_btn;
lv_obj_t *water_led, *light_led, *air_led;

// If logging is enabled, it will inform the user about what is happening in the library
void log_print(lv_log_level_t level, const char * buf) {
  LV_UNUSED(level);
  Serial.println(buf);
  Serial.flush();
}

/* ---------------- TOUCH READ ---------------- */
void touchscreen_read(lv_indev_t * indev, lv_indev_data_t * data) {
  // Checks if Touchscreen was touched, and prints X, Y and Pressure (Z)
  if(touchscreen.tirqTouched() && touchscreen.touched()) {
    // Get Touchscreen points
    TS_Point p = touchscreen.getPoint();
    // Calibrate Touchscreen points with map function to the correct width and height
    int x = map(p.x, 200, 3700, 1, SCREEN_WIDTH);
    int y = map(p.y, 240, 3800, 1, SCREEN_HEIGHT);

    data->state = LV_INDEV_STATE_PRESSED;

    // Set the coordinates
    data->point.x = x;
    data->point.y = y;

    // Print Touchscreen info about X, Y and Pressure (Z) on the Serial Monitor
    Serial.print("X = ");
    Serial.print(x);
    Serial.print(" | Y = ");
    Serial.print(y);
    Serial.println();
  }
  else {
    data->state = LV_INDEV_STATE_RELEASED;
  }
}

/* ---------------- LED ---------------- */
void set_led(lv_obj_t *led, bool on) {
  lv_obj_set_style_bg_color(
    led, on ? lv_color_hex(0x00FF00) : lv_color_hex(0xFF0000), 0
  );
}

/* ---------------- CALLBACKS ---------------- */
static void water_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    watering_active = !watering_active;
    set_led(water_led, watering_active);
    lv_label_set_text(lv_obj_get_child(water_btn, 0),
                      watering_active ? "ON" : "OFF");
    LV_LOG_USER("Watering System %s", watering_active ? "ON" : "OFF");
  }
}

static void light_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    lighting_active = !lighting_active;
    set_led(light_led, lighting_active);
    lv_label_set_text(lv_obj_get_child(light_btn, 0),
                      lighting_active ? "ON" : "OFF");
    LV_LOG_USER("Lighting System %s", lighting_active ? "ON" : "OFF");
  }
}

static void air_cb(lv_event_t * e) {
  lv_event_code_t code = lv_event_get_code(e);
  if(code == LV_EVENT_CLICKED) {
    air_active = !air_active;
    set_led(air_led, air_active);
    lv_label_set_text(lv_obj_get_child(air_btn, 0),
                      air_active ? "ON" : "OFF");
    LV_LOG_USER("Air Quality System %s", air_active ? "ON" : "OFF");
  }
}

/* ---------------- DASHBOARD ---------------- */
void dashboard_row(lv_obj_t *parent, int y, const char *label, const char *value, lv_color_t indicator_color) {
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

  // Value on the right
  lv_obj_t *val = lv_label_create(row);
  lv_label_set_text(val, value);
  lv_obj_set_style_text_color(val, lv_color_hex(0x000000), 0);
  lv_obj_set_style_text_font(val, &lv_font_montserrat_14, 0);
  lv_obj_align(val, LV_ALIGN_RIGHT_MID, -30, 0);

  // Color indicator circle
  lv_obj_t *indicator = lv_obj_create(row);
  lv_obj_set_size(indicator, 16, 16);
  lv_obj_align(indicator, LV_ALIGN_RIGHT_MID, -6, 0);
  lv_obj_set_style_radius(indicator, LV_RADIUS_CIRCLE, 0);
  lv_obj_set_style_bg_color(indicator, indicator_color, 0);
  lv_obj_set_style_border_width(indicator, 0, 0);
}

void create_dashboard(lv_obj_t *parent) {
  dashboard_row(parent, 15,  "Temperature", "24.5°C", lv_color_hex(0xFF6B35));
  dashboard_row(parent, 65,  "Humidity", "65%", lv_color_hex(0x4D96FF));
  dashboard_row(parent, 115, "Soil Moisture", "45%", lv_color_hex(0x8D6E63));
  dashboard_row(parent, 165, "Water Level", "75%", lv_color_hex(0x1E88E5));
}

/* ---------------- CONTROL ROW ---------------- */
void control_row(lv_obj_t *parent, int y, const char *name,
                 lv_event_cb_t cb,
                 lv_obj_t **btn, lv_obj_t **led) {

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
  lv_obj_set_size(*btn, 60, 26);
  lv_obj_align(*btn, LV_ALIGN_RIGHT_MID, -30, 0);
  lv_obj_add_event_cb(*btn, cb, LV_EVENT_CLICKED, NULL);
  lv_obj_clear_flag(*btn, LV_OBJ_FLAG_GESTURE_BUBBLE);

  lv_obj_t *btxt = lv_label_create(*btn);
  lv_label_set_text(btxt, "OFF");
  lv_obj_center(btxt);

  *led = lv_obj_create(row);
  lv_obj_set_size(*led, 14, 14);
  lv_obj_align(*led, LV_ALIGN_RIGHT_MID, -6, 0);
  lv_obj_set_style_radius(*led, LV_RADIUS_CIRCLE, 0);
  set_led(*led, false);
}

/* ---------------- CONTROLS ---------------- */
void create_controls(lv_obj_t *parent) {
  control_row(parent, 20,  "Watering System", water_cb,
              &water_btn, &water_led);
  control_row(parent, 70,  "Lighting System", light_cb,
              &light_btn, &light_led);
  control_row(parent, 120, "Air Quality System", air_cb,
              &air_btn, &air_led);
}

/* ---------------- GUI ---------------- */
void create_gui() {
  tabview = lv_tabview_create(lv_screen_active());
  // Use rotated dimensions for the tabview
  lv_obj_set_size(tabview, ROTATED_WIDTH, ROTATED_HEIGHT);
  lv_tabview_set_tab_bar_size(tabview, 26);

  lv_obj_t *dash = lv_tabview_add_tab(tabview, "Dashboard");
  lv_obj_t *ctrl = lv_tabview_add_tab(tabview, "Controls");

  /* push content below tab bar */
  lv_obj_set_style_pad_top(dash, 8, 0);
  lv_obj_set_style_pad_top(ctrl, 8, 0);

  create_dashboard(dash);
  create_controls(ctrl);
}

/* ---------------- SETUP ---------------- */
void setup() {
  String LVGL_Arduino = String("LVGL Library Version: ") + lv_version_major() + "." + lv_version_minor() + "." + lv_version_patch();
  Serial.begin(115200);
  Serial.println(LVGL_Arduino);
  Serial.println("Smart Greenhouse Control System");
  
  lv_init();
  // Register print function for debugging
  lv_log_register_print_cb(log_print);

  touchscreenSPI.begin(XPT2046_CLK, XPT2046_MISO,
                       XPT2046_MOSI, XPT2046_CS);
  touchscreen.begin(touchscreenSPI);
  touchscreen.setRotation(2);

  lv_display_t *disp = lv_tft_espi_create(
    SCREEN_WIDTH, SCREEN_HEIGHT, draw_buf, sizeof(draw_buf)
  );
  lv_display_set_rotation(disp, LV_DISPLAY_ROTATION_270);

  lv_indev_t *indev = lv_indev_create();
  lv_indev_set_type(indev, LV_INDEV_TYPE_POINTER);
  lv_indev_set_read_cb(indev, touchscreen_read);

  create_gui();
}

/* ---------------- LOOP ---------------- */
void loop() {
  lv_task_handler();  // let the GUI do its work
  lv_tick_inc(5);     // tell LVGL how much time has passed
  delay(5);           // let this time pass
}
