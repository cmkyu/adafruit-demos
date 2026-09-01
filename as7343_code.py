import time
import board
import digitalio
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
import adafruit_as7343

# Turn on the TFT / STEMMA QT power supply pin (required on the ESP32-S2 TFT Feather)
if hasattr(board, "TFT_I2C_POWER"):
    tft_power = digitalio.DigitalInOut(board.TFT_I2C_POWER)
    tft_power.direction = digitalio.Direction.OUTPUT
    tft_power.value = True
    time.sleep(0.1)

# Use the built-in display native to the ESP32-S2 TFT Feather
display = board.DISPLAY

# Root display group
main_group = displayio.Group()
display.root_group = main_group

# Initialize I2C and AS7343 sensor
i2c = board.I2C()
try:
    as7343 = adafruit_as7343.AS7343(i2c)
except Exception as e:
    err_group = displayio.Group()
    err_label = label.Label(terminalio.FONT, text="AS7343 not found!", color=0xFF0000, scale=2)
    err_label.x = 20
    err_label.y = 60
    err_group.append(err_label)
    display.root_group = err_group
    while True:
        time.sleep(0.1)

# Configure sensor parameters
as7343.gain = adafruit_as7343.Gain.X64
as7343.atime = 29
as7343.astep = 599

# 12 spectral channels configuration
NUM_BARS = 12
CHANNEL_KEYS = [
    "F1", "F2", "FZ", "F3", "F4", "F5",
    "FY", "FXL", "F6", "F7", "F8", "NIR"
]

# 24-bit RGB hex colors matching the spectral channel wavelengths
BAR_COLORS = [
    0x8A2BE2, # F1  405nm violet
    0x4B0082, # F2  425nm blue-violet
    0x0000FF, # FZ  450nm blue
    0x00BFFF, # F3  475nm cyan-blue
    0x00FF00, # F4  515nm green
    0xADFF2F, # F5  550nm yellow-green
    0xFFFF00, # FY  555nm yellow
    0xFFA500, # FXL 600nm orange
    0xFF0000, # F6  640nm red (True Red)
    0xB22222, # F7  690nm deep red
    0x8B0000, # F8  745nm dark red
    0x550000, # NIR 855nm maroon
]

# Chart geometry layout for the 240x135 display
BAR_TOP = 24
BAR_BOTTOM = 118
BAR_LEFT = 4
BAR_WIDTH = 17
BAR_GAP = 3
BAR_HEIGHT = BAR_BOTTOM - BAR_TOP

# Build initial UI components group
ui_group = displayio.Group()

# Title label
title_label = label.Label(terminalio.FONT, text="AS7343 Spectrum", color=0xFFFFFF, scale=1)
title_label.x = 65
title_label.y = 10
ui_group.append(title_label)

# Create dynamic visual elements for bars, values, and channel labels
bar_rects = []
val_labels = []
cat_labels = []

for i in range(NUM_BARS):
    x_pos = BAR_LEFT + i * (BAR_WIDTH + BAR_GAP)
    
    # Placeholder rectangle for the bar
    rect = Rect(x=x_pos, y=BAR_BOTTOM, width=BAR_WIDTH, height=1, fill=BAR_COLORS[i])
    bar_rects.append(rect)
    ui_group.append(rect)
    
    # Value label on top of the bar
    v_label = label.Label(terminalio.FONT, text="", color=0xFFFFFF, scale=1)
    v_label.x = x_pos
    v_label.y = BAR_TOP - 6
    val_labels.append(v_label)
    ui_group.append(v_label)
    
    # Channel label underneath the bar
    c_label = label.Label(terminalio.FONT, text=CHANNEL_KEYS[i], color=BAR_COLORS[i], scale=1)
    c_label.x = x_pos + 1
    c_label.y = BAR_BOTTOM + 8
    cat_labels.append(c_label)
    ui_group.append(c_label)

main_group.append(ui_group)

# Main loop
while True:
    try:
        all_readings = as7343.all_channels
        # Map your CHANNEL_KEYS to the correct indices from all_readings
        channel_values = [
            all_readings[12],  # F1
            all_readings[6],   # F2
            all_readings[0],   # FZ
            all_readings[7],   # F3
            all_readings[8],   # F4
            all_readings[15],  # F5
            all_readings[1],   # FY
            all_readings[2],   # FXL
            all_readings[9],   # F6
            all_readings[13],  # F7
            all_readings[14],  # F8
            all_readings[3],   # NIR
        ]
    except Exception as err:
        print("Sensor read failed:", err)
        time.sleep(0.5)
        continue

    # Find max value for auto-scaling
    max_val = 1
    for val in channel_values:
        if val > max_val:
            max_val = val

    # Update bars and labels dynamically
    for i in range(NUM_BARS):
        val = channel_values[i]
        h = int(val * BAR_HEIGHT // max_val)
        # Ensure minimum height of 1 pixel to avoid ValueError
        if h < 1:
            h = 1
        
        y_pos = BAR_BOTTOM - h
        x_pos = BAR_LEFT + i * (BAR_WIDTH + BAR_GAP)
        
        # Remove old rectangle
        old_rect = bar_rects[i]
        ui_group.remove(old_rect)
        
        # Create new rectangle with updated dimensions
        new_rect = Rect(x=x_pos, y=y_pos, width=BAR_WIDTH, height=h, fill=BAR_COLORS[i])
        bar_rects[i] = new_rect
        
        # Insert the new rectangle at the correct position in the group
        ui_group.insert(0, new_rect)
        
        # Update value text
        val_str = str(val)
        val_labels[i].text = val_str
        val_labels[i].x = max(BAR_LEFT, (BAR_LEFT + i * (BAR_WIDTH + BAR_GAP)) + (BAR_WIDTH - len(val_str) * 6) // 2)
        
        # Keep value label pinned inside the top boundary viewable area
        v_y = y_pos - 6
        val_labels[i].y = v_y if v_y >= BAR_TOP else BAR_TOP

    time.sleep(0.2)
