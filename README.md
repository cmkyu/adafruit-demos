# Sensor Display Demos for Adafruit ESP32-S2 TFT Feather

> **⚠️ Disclaimer:** These code examples were generated with AI assistance and are provided "as-is" for educational and reference purposes. They may contain bugs or require adjustments for your specific hardware setup. Use them at your own risk. Always test thoroughly before relying on them in any critical application.

## Overview

This repository contains three display demo programs for the **Adafruit ESP32-S2 TFT Feather** board, each designed to work with a different I2C sensor via the STEMMA QT / Qwiic connector. Each program reads sensor data and displays it on the built-in 240x135 pixel color TFT display.

## Common Hardware Requirements

All examples require:
- **Adafruit ESP32-S2 TFT Feather** – [Product Link](https://www.adafruit.com/product/5300)
- A **STEMMA QT / Qwiic JST SH 4-pin Cable** – [Product Link](https://www.adafruit.com/product/4399)
- **USB-C Cable** capable of data transfer.

## File-Specific Hardware & Prerequisites

### 1. `as7343_code.py` – AS7343 14-Channel Light / Color Sensor

**Required Hardware:**
- **Adafruit AS7343 14-Channel Light / Color Sensor Breakout** – [Product Link](https://www.adafruit.com/product/5404)

**CircuitPython Libraries Needed:**
- `adafruit_as7343`
- `adafruit_display_shapes`
- `adafruit_display_text`

**Installation:**
```bash
circup install adafruit_as7343 adafruit_display_shapes adafruit_display_text
```

**Features:**
- Displays a 12-channel spectral bar graph
- Auto-scaling bars based on maximum reading
- Shows channel labels (F1, F2, FZ, etc.) with color-matched text
- Displays raw sensor values above each bar

### 2. `ltr390_code.py` – LTR390 UV / Light Sensor

**Required Hardware:**
- **Adafruit LTR390 UV / Light Sensor** – [Product Link](https://www.adafruit.com/product/4831)

**CircuitPython Libraries Needed:**
- `adafruit_ltr390`
- `adafruit_display_text`

**Installation:**
```bash
circup install adafruit_ltr390 adafruit_display_text
```

**Features:**
- Displays UV index reading
- Displays ambient light (ALS) reading

### 3. `veml7700_code.py` – VEML7700 Ambient Light Sensor

**Required Hardware:**
- **Adafruit VEML7700 Ambient Light Sensor** – [Product Link](https://www.adafruit.com/product/4162)

**CircuitPython Libraries Needed:**
- `adafruit_veml7700`
- `adafruit_display_text`

**Installation:**
```bash
circup install adafruit_veml7700 adafruit_display_text
```

**Features:**
- Displays ambient light in lux

## Common Setup Instructions

1. **Install CircuitPython** on your ESP32-S2 TFT Feather following the [official guide](https://learn.adafruit.com/adafruit-esp32-s2-tft-feather/circuitpython).

2. **Install Required Libraries** using circup or by manually copying from the [Adafruit CircuitPython Library Bundle](https://circuitpython.org/libraries).

3. **Connect the Sensor**: Use the STEMMA QT cable to connect your sensor to the STEMMA QT port on the Feather board.

4. **Upload Code**: Copy the desired `.py` file to your board as `code.py` (or use a different name and import it).

5. **Run**: The program will start automatically on boot or reset.

## Modifying the Code

### Changing Sensor Gain/Integration Time
For `as7343_code.py`, modify these lines:
```python
as7343.gain = adafruit_as7343.Gain.X64  # Change gain
as7343.atime = 29                       # Integration time
as7343.astep = 599                      # Step time
```

### Adjusting Update Rate
Change the value in `time.sleep()` at the end of each main loop:
```python
time.sleep(0.2)  # 200ms update rate
```

## License & Attribution

These examples are provided for educational purposes. The code uses Adafruit's CircuitPython libraries which are open-source and maintained by the Adafruit community.

## References

- [Adafruit ESP32-S2 TFT Feather Guide](https://learn.adafruit.com/adafruit-esp32-s2-tft-feather)
- [CircuitPython Documentation](https://circuitpython.org/)
- [Adafruit AS7343 Documentation](https://learn.adafruit.com/adafruit-as7343)
- [Adafruit LTR390 Documentation](https://learn.adafruit.com/adafruit-ltr390)
- [Adafruit VEML7700 Documentation](https://learn.adafruit.com/adafruit-veml7700)

---

*Last Updated: August 2026*
