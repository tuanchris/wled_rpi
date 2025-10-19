# WLED Effects for Raspberry Pi

A Python implementation of WLED effects for Raspberry Pi using the neopixel library. This project ports WLED's extensive effect library and palette system to run on Raspberry Pi with NeoPixel LED strips.

## Features

- **16 Core Effects**: Static, Blink, Breathe, Rainbow, Scan, Theater Chase, Sparkle, and more
- **59 Color Palettes**: All WLED gradient palettes including Sunset, Fire, Aurora, Rainbow, etc.
- **Full WLED Compatibility**: Effects behave identically to WLED
- **Easy to Use**: Simple CLI interface with argparse
- **Extensible**: Easy to add new effects

## Hardware Requirements

- Raspberry Pi (any model with GPIO)
- WS2812B/NeoPixel LED strip
- Appropriate power supply for LEDs

## Installation

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install python3-pip
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

## Quick Start

Run the default rainbow effect:
```bash
python3 wled_controller.py
```

Run a specific effect:
```bash
python3 wled_controller.py --effect 1 --speed 200
```

List all available effects:
```bash
python3 wled_controller.py --list-effects
```

List all available palettes:
```bash
python3 wled_controller.py --list-palettes
```

## Usage

```
python3 wled_controller.py [OPTIONS]

Options:
  --num NUM               Number of LEDs (default: 60)
  --brightness FLOAT      Brightness 0.0-1.0 (default: 0.35)
  --effect, -e ID         Effect ID (default: 8 = Rainbow Cycle)
  --speed, -s SPEED       Effect speed 0-255 (default: 128)
  --intensity, -i INT     Effect intensity 0-255 (default: 128)
  --palette, -p ID        Palette ID 0-58 (default: 0)
  --order ORDER           Pixel order: GRB, RGB, BRG, RGBW, GRBW (default: GRB)
  --pin PIN               Board pin e.g. D18 = GPIO18 (default: D18)
  --list-effects          List all available effects
  --list-palettes         List all available palettes
```

## Available Effects

| ID | Effect Name | Description |
|----|-------------|-------------|
| 0  | Static      | Solid color |
| 1  | Blink       | Blink between two colors |
| 2  | Breathe     | Breathing effect |
| 3  | Wipe        | Color wipe across strip |
| 4  | Fade        | Fade between colors |
| 5  | Scan        | Single LED scanning |
| 6  | Dual Scan   | Two LEDs scanning |
| 7  | Rainbow     | Solid rainbow (cycles hue) |
| 8  | Rainbow Cycle | Rainbow distributed across strip |
| 9  | Theater Chase | Theater-style chase |
| 10 | Running Lights | Sine wave running lights |
| 11 | Random Color | Random solid colors |
| 12 | Dynamic     | Random colors per pixel |
| 13 | Twinkle     | Twinkling stars |
| 14 | Sparkle     | Single random sparkle |
| 15 | Strobe      | Strobe effect |

## Examples

### Rainbow Effect (like your original fx009)
```bash
python3 wled_controller.py --effect 8 --speed 20 --num 60
```

### Fire Effect with Fire Palette
```bash
python3 wled_controller.py --effect 13 --palette 22 --speed 100
```

### Breathe Effect
```bash
python3 wled_controller.py --effect 2 --speed 50 --intensity 200
```

### Theater Chase
```bash
python3 wled_controller.py --effect 9 --speed 150
```

## Color Palettes

The system includes all 59 WLED gradient palettes:
- Sunset, Rivendell, Breeze, Fire, Icefire
- Aurora, Aurora 2, Temperature
- C9 (Christmas lights), Traffic Light
- Ocean, Forest, Lava, Cloud
- And 45 more!

Use `--list-palettes` to see all available options.

## Project Structure

```
wled_rpi_backend/
├── wled_controller.py      # Main controller script
├── segment.py               # Segment class (manages LED strip)
├── effects/
│   ├── __init__.py
│   └── basic_effects.py    # Effect implementations
├── utils/
│   ├── __init__.py
│   ├── colors.py           # Color manipulation functions
│   └── palettes.py         # All 59 WLED palettes
└── README.md
```

## API Usage

You can also use this as a library in your own Python scripts:

```python
import board
import neopixel
from segment import Segment
from effects.basic_effects import mode_rainbow_cycle

# Setup
pixels = neopixel.NeoPixel(board.D18, 60, brightness=0.35, auto_write=False)
segment = Segment(pixels, 0, 60)

# Configure
segment.speed = 128
segment.intensity = 128

# Run effect
while True:
    delay = mode_rainbow_cycle(segment)
    pixels.show()
    time.sleep(delay / 1000.0)
```

## Wiring

Connect your NeoPixel strip to the Raspberry Pi:
- LED Data → GPIO18 (Pin 12) [or your chosen pin]
- LED GND → GND
- LED 5V → External 5V power supply

**Important**: Use an external power supply for the LEDs, not the Pi's 5V rail!

## Adding Custom Effects

Create new effects by following the pattern in `effects/basic_effects.py`:

```python
def mode_my_effect(seg: Segment) -> int:
    """My custom effect"""
    # Your effect code here
    # Access seg.speed, seg.intensity, seg.length, etc.
    # Use seg.set_pixel_color(i, color) to set pixels

    return FRAMETIME  # Return delay in milliseconds
```

Then add it to the EFFECTS dictionary.

## Credits

- Original WLED project: https://github.com/Aircoookie/WLED
- Effects and palettes ported from WLED firmware
- Built for Raspberry Pi with love ❤️

## License

This project maintains compatibility with WLED's licensing while being a separate implementation.
