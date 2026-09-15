# J4, J5 and J6 connector guide

Pin numbers are KiCad pad numbers, not left-to-right positions in a rotated board view. Locate pad 1 before wiring.

## J4 — Future microphone-ring interface

PDM x4, clock, I2C, spare GPIO, 3.3 V and grounds

| Pin | Signal |
| --- | --- |
| 1 | 3V3 |
| 2 | GND |
| 3 | PDM_CLK |
| 4 | GND |
| 5 | PDM_DATA0_CONN |
| 6 | GND |
| 7 | PDM_DATA1_CONN |
| 8 | GND |
| 9 | PDM_DATA2_CONN |
| 10 | GND |
| 11 | PDM_DATA3_CONN |
| 12 | I2C_SDA |
| 13 | I2C_SCL |
| 14 | RING_GPIO_SPARE |

## J5 — ESP32 serial programming and debug

UART0 TX/RX, BOOT, EN, GND, 3V3

| Pin | Signal |
| --- | --- |
| 1 | 3V3 |
| 2 | GND |
| 3 | UART0_TX |
| 4 | ESP_EN |
| 5 | UART0_RX |
| 6 | BOOT_GPIO0 |

## J6 — I2C and GPIO expansion

3V3, GND, SDA, SCL and two PCAL GPIO

| Pin | Signal |
| --- | --- |
| 1 | 3V3 |
| 2 | GND |
| 3 | I2C_SDA |
| 4 | I2C_SCL |
| 5 | EXP_GPIO0 |
| 6 | EXP_GPIO1 |

J4 is reserved for the future ring. Its header and signal names do not establish a completed eight-microphone capture system. Ring capture hardware, interface and firmware remain to be designed.

J5 carries 3.3 V logic-level UART signals. It is not a USB connector. J6 exposes two GPIO-expander signals alongside the shared I2C bus.