import smbus
import time

# I2C Address (Check using `i2cdetect -y 1`)
I2C_ADDR = 0x27

# LCD Constants
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

# Timing Constants
ENABLE = 0b00000100
E_DELAY = 0.0005

class lcd:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.lcd_init()

    def lcd_init(self):
        self.lcd_byte(0x33, LCD_CMD)
        self.lcd_byte(0x32, LCD_CMD)
        self.lcd_byte(0x28, LCD_CMD)
        self.lcd_byte(0x0C, LCD_CMD)
        self.lcd_byte(0x06, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        BACKLIGHT = 0x08  # Turn backlight on
        high_bits = mode | (bits & 0xF0) | ENABLE
        low_bits = mode | ((bits << 4) & 0xF0) | ENABLE

        self.bus.write_byte(I2C_ADDR, high_bits)
        self.lcd_toggle_enable(high_bits)

        self.bus.write_byte(I2C_ADDR, low_bits)
        self.lcd_toggle_enable(low_bits)

 def lcd_toggle_enable(self, bits):
    time.sleep(E_DELAY)
    self.bus.write_byte(I2C_ADDR, (bits & ~ENABLE) | BACKLIGHT)
    time.sleep(E_DELAY)

def lcd_display_string(self, message, line):
    message = message.ljust(LCD_WIDTH, " ")
    if line == 1:
        self.lcd_byte(LCD_LINE_1, LCD_CMD)
    elif line == 2:
        self.lcd_byte(LCD_LINE_2, LCD_CMD)

    for char in message:
        self.lcd_byte(ord(char), LCD_CHR)

    def lcd_clear(self):
        self.lcd_byte(0x01, LCD_CMD)
