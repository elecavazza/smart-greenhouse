/*  Automated Indoor Greenhouse Control System UI
    ESP32-2432S028R (Cheap Yellow Display)
    240x320 rotated 270° → logical 320x240
*/

#include <lvgl.h>
#include <TFT_eSPI.h>
#include <XPT2046_Touchscreen.h>

/* ---------------- TOUCH ---------------- */
#define XPT2046_IRQ 36
#define XPT2046_MOSI 32
#define XPT2046_MISO 39
#define XPT2046_CLK 25
#define XPT2046_CS 33

SPIClass touchscreenSPI = SPIClass(VSPI);
XPT2046_Touchscreen touchscreen(XPT2046_CS, XPT2046_IRQ);

/* ---------------- DISPLAY ---------------- */
#define DISP_W 320
#define DISP_H 240

#define DRAW_BUF_SIZE (DISP_W * DISP_H / 10 * (LV_COLOR_DEPTH / 8))
uint32_t draw_buf[DRAW_BUF_SIZE / 4];

/* ---------------- STATES ---------------- */
bool watering_active = false;
bool lighting_active = false;
bool air_active      = false;

/* ---------------- SENSOR MOCK ---------------- */
float temperature = 24.5;
float humidity = 65;
int voc = 125;
int soil = 45;
int water = 75;

/* ---------------- UI ---------------- */
lv_obj_t *tabview;

lv_obj_t *temp_lbl;
lv_obj_t *hum_lbl;
lv_obj_t *voc_lbl;
lv_obj_t *soil_lbl;
lv_obj_t *water_lbl;

lv_obj_t *water_btn;
lv_obj_t *light_btn;
lv_obj_t *air_btn;

lv_obj_t *water_led;
lv_obj_t *light_led;
lv_obj_t *air_led;

/* ---------------- TOUCH READ ---------------- */
void touchscreen_read(lv_indev_t * indev, lv_indev_data_t * data) {
  if (touchscreen.tirqTouched() && touchscreen.touched()) {
    TS_Point p = touchscreen.getPoint();
    data->state = LV_INDEV_STATE_PRESSED;
    data->point.x = map(p.x, 200, 3700, 0, DISP_W);
    data->point.y = map(p.y, 240, 3800, 0, DISP_H);
  } else {
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
  watering_active = !watering_active;
  set_led(water_led, watering_active);
  lv_label_set_text(lv_obj_get_child(water_btn, 0),
                    watering_active ? "ON" : "OFF");
}

static void light_cb(lv_event_t * e) {
  lighting_active = !lighting_active;
  set_led(light_led, lighting_active);
  lv_label_set_text(lv_obj_get_child(light_btn, 0),
                    lighting_active ? "ON" : "OFF");
}

static void air_cb(lv_event_t * e) {
  air_active = !air_active;
  set_led(air_led, air_active);
  lv_label_set_text(lv_obj_get_child(air_btn, 0),
                    air_active ? "ON" : "OFF");
}

/* ---------------- DASHBOARD ---------------- */
void dashboard_row(lv_obj_t *parent, int y, lv_color_t c,
                   const char *txt, lv_obj_t **lbl) {

  lv_obj_t *box = lv_obj_create(parent);
  lv_obj_set_width(box, lv_pct(100));      // FIXED WIDTH
  lv_obj_set_height(box, 32);
  lv_obj_set_pos(box, 0, y);
  lv_obj_set_style_bg_color(box, c, 0);
  lv_obj_set_style_pad_all(box, 4, 0);

  *lbl = lv_label_create(box);
  lv_label_set_text(*lbl, txt);
  lv_obj_align(*lbl, LV_ALIGN_LEFT_MID, 6, 0);
}

void create_dashboard(lv_obj_t *parent) {
  int y = 8;

  dashboard_row(parent, y, lv_color_hex(0xFF6B35),
                "Temp: 24.5 C", &temp_lbl); y += 36;
  dashboard_row(parent, y, lv_color_hex(0x4D96FF),
                "Humidity: 65 %", &hum_lbl); y += 36;
  dashboard_row(parent, y, lv_color_hex(0x9B59B6),
                "VOC: 125 ppb", &voc_lbl); y += 36;
  dashboard_row(parent, y, lv_color_hex(0x8D6E63),
                "Soil: 45 %", &soil_lbl); y += 36;
  dashboard_row(parent, y, lv_color_hex(0x1E88E5),
                "Water: 75 %", &water_lbl);
}

/* ---------------- ONE-LINE CONTROL ---------------- */
void control_row(lv_obj_t *parent, int y, const char *name,
                 lv_event_cb_t cb,
                 lv_obj_t **btn, lv_obj_t **led) {

  lv_obj_t *row = lv_obj_create(parent);
  lv_obj_set_width(row, lv_pct(100));       // FIXED WIDTH
  lv_obj_set_height(row, 36);
  lv_obj_set_pos(row, 0, y);
  lv_obj_set_style_pad_all(row, 4, 0);

  lv_obj_t *lbl = lv_label_create(row);
  lv_label_set_text(lbl, name);
  lv_obj_align(lbl, LV_ALIGN_LEFT_MID, 4, 0);

  *btn = lv_button_create(row);
  lv_obj_set_size(*btn, 60, 26);
  lv_obj_align(*btn, LV_ALIGN_RIGHT_MID, -30, 0);
  lv_obj_add_event_cb(*btn, cb, LV_EVENT_CLICKED, NULL);

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
  lv_obj_set_size(tabview, DISP_W, DISP_H);
  lv_tabview_set_tab_bar_size(tabview, 26);

  /* 🔧 FIX: Make tab bar clickable */
  lv_obj_t *tab_bar = lv_tabview_get_tab_bar(tabview);
  lv_obj_remove_flag(tab_bar, LV_OBJ_FLAG_SCROLLABLE);
  lv_obj_clear_flag(tab_bar, LV_OBJ_FLAG_GESTURE_BUBBLE);

  lv_obj_t *dash = lv_tabview_add_tab(tabview, "Dashboard");
  lv_obj_t *ctrl = lv_tabview_add_tab(tabview, "Controls");

  lv_obj_remove_flag(dash, LV_OBJ_FLAG_SCROLLABLE);
  lv_obj_remove_flag(ctrl, LV_OBJ_FLAG_SCROLLABLE);

  create_dashboard(dash);
  create_controls(ctrl);
}

/* ---------------- SETUP ---------------- */
void setup() {
  lv_init();

  touchscreenSPI.begin(XPT2046_CLK, XPT2046_MISO,
                       XPT2046_MOSI, XPT2046_CS);
  touchscreen.begin(touchscreenSPI);
  touchscreen.setRotation(2);

  lv_display_t *disp = lv_tft_espi_create(
    240, 320, draw_buf, sizeof(draw_buf)
  );
  lv_display_set_rotation(disp, LV_DISPLAY_ROTATION_270);

  lv_indev_t *indev = lv_indev_create();
  lv_indev_set_type(indev, LV_INDEV_TYPE_POINTER);
  lv_indev_set_read_cb(indev, touchscreen_read);

  create_gui();
}

/* ---------------- LOOP ---------------- */
void loop() {
  lv_tick_inc(5);
  lv_task_handler();
  delay(5);
}
