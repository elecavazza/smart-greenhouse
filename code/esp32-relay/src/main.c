#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

// Relay control pin - connected to relay module IN pin
// Using GPIO4 (labeled D2 on Seeed XIAO ESP32-C3)
// Avoiding GPIO2 as it has boot mode functions
#define RELAY_PIN GPIO_NUM_4

void app_main(void) {
    // Configure GPIO as output for relay control
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << RELAY_PIN),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    gpio_config(&io_conf);
    
    // Initialize relay to OFF state (HIGH for active-low relay)
    gpio_set_level(RELAY_PIN, 1);
    
    printf("Relay Control Started on GPIO %d (D2) - Active-Low Mode\n", RELAY_PIN);
    printf("\nWiring Instructions:\n");
    printf("  Relay IN  -> ESP32-C3 GPIO4 (D2 pin)\n");
    printf("  Relay GND -> ESP32-C3 GND pin\n");
    printf("  Relay VCC -> ESP32-C3 5V pin (recommended) OR 3.3V pin\n");
    printf("\nNote on VCC:\n");
    printf("  - Most relay modules need 5V to operate reliably\n");
    printf("  - 5V comes from USB power on ESP32-C3\n");
    printf("  - Only use 3.3V if your relay module specifically supports it\n");
    printf("  - The GPIO2 control signal is 3.3V (relay module handles this)\n\n");
    
    // Infinite loop to toggle relay every 2 seconds
    // Note: Most relay modules are active-low (LOW = ON, HIGH = OFF)
    while (1) {
        // Turn relay ON (LOW signal for active-low relay)
        gpio_set_level(RELAY_PIN, 0);
        printf("Relay ON\n");
        vTaskDelay(pdMS_TO_TICKS(2000));  // Wait 2 seconds
        
        // Turn relay OFF (HIGH signal for active-low relay)
        gpio_set_level(RELAY_PIN, 1);
        printf("Relay OFF\n");
        vTaskDelay(pdMS_TO_TICKS(2000));  // Wait 2 seconds
    }
}