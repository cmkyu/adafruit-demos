import time
import board
import terminalio
from adafruit_display_text import bitmap_label
import displayio
import adafruit_veml7700

# Initialize I2C and the VEML7700 sensor
# (Works with the built-in STEMMA QT connector or standard SDA/SCL pins)
i2c = board.I2C()
veml = adafruit_veml7700.VEML7700(i2c)

# Optional: Adjust integration time or gain if needed
# veml.gain = adafruit_veml7700.VEML7700_GAIN_1
# veml.integration_time = adafruit_veml7700.VEML7700_IT_100MS

display = board.DISPLAY

# Create text label for the lux reading
text_area = bitmap_label.Label(terminalio.FONT, text="LUX: Reading...", scale=2)
text_area.x = 10
text_area.y = 50

# Set up the display group (CircuitPython 9/10 syntax)
main_group = displayio.Group()
main_group.append(text_area)
display.root_group = main_group

while True:
    try:
        # Read the current lux value from the sensor
        current_lux = veml.lux
        text_area.text = f"LUX: {current_lux:.1f}"
    except RuntimeError:
        # Sometimes sensor reads can briefly fail; catch it to prevent crashes
        text_area.text = "Sensor Error"

    time.sleep(0.5)
