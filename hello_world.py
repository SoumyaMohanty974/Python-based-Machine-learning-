from machine import Pin, SoftI2C
import ssd1306

# Define I2C pins
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Initialize the OLED display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Clear the display
oled.fill(0)
oled.show()

# Write "Hello, World!" to the OLED display
oled.text("Hello, World!", 0, 0)
oled.show()
