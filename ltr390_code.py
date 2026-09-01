# ESP32-S2 TFT Feather + Adafruit LTR390
# Displays the same basic information as the reference:
#
#   LTR390 Demo
#   UV: 1
#   ALS: 410
#
# Required CircuitPython libraries:
#   adafruit_ltr390
#   adafruit_display_text

import time
import board
import displayio
import terminalio

from adafruit_display_text.bitmap_label import Label
import adafruit_ltr390


# LTR390 connected to the Feather's STEMMA QT port.
try:
    i2c = board.STEMMA_I2C()
except AttributeError:
    i2c = board.I2C()

ltr = adafruit_ltr390.LTR390(i2c)


root = displayio.Group()

title = Label(
    terminalio.FONT,
    text="LTR390 Demo",
    scale=2,
    color=0xFFFFFF,
)
title.x = 40
title.y = 32

uv_text = Label(
    terminalio.FONT,
    text="UV: --",
    scale=2,
    color=0xFFFFFF,
)
uv_text.x = 40
uv_text.y = 65

als_text = Label(
    terminalio.FONT,
    text="ALS: --",
    scale=2,
    color=0xFFFFFF,
)
als_text.x = 40
als_text.y = 98

root.append(title)
root.append(uv_text)
root.append(als_text)

board.DISPLAY.root_group = root


while True:
    uv = ltr.uvs
    als = ltr.light

    uv_text.text = f"UV: {uv}"
    als_text.text = f"ALS: {als}"

    print(f"UV: {uv}    ALS: {als}")

    time.sleep(0.5)
