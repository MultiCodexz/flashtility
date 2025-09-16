# app/src/tools/oled_display.py
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306

def init_oled():
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
    return device
