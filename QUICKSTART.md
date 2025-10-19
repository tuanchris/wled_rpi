# Quick Start Guide

## Installation

1. **Install dependencies**:
```bash
pip3 install -r requirements.txt
```

2. **Make scripts executable**:
```bash
chmod +x wled_controller.py example.py
```

## Run Your First Effect

### Rainbow Effect (matching your original fx009)
```bash
python3 wled_controller.py --effect 8 --speed 20 --num 60 --brightness 0.35
```

This runs the Rainbow Cycle effect with:
- 60 LEDs
- Speed 20 (matches your original example)
- 35% brightness
- Default pin GPIO18

### List All Effects
```bash
python3 wled_controller.py --list-effects
```

### Try Different Effects

**Breathe** (smooth pulsing):
```bash
python3 wled_controller.py --effect 2 --speed 50
```

**Theater Chase** (classic LED chase):
```bash
python3 wled_controller.py --effect 9 --speed 150
```

**Twinkle** (starfield effect):
```bash
python3 wled_controller.py --effect 13 --speed 100 --intensity 128
```

**Fire** (with Fire palette):
```bash
python3 wled_controller.py --effect 13 --palette 22 --speed 100
```

## Common Options

| Option | Description | Range |
|--------|-------------|-------|
| `--effect` or `-e` | Effect ID | 0-15 |
| `--speed` or `-s` | Animation speed | 0-255 (higher = faster) |
| `--intensity` or `-i` | Effect intensity | 0-255 |
| `--palette` or `-p` | Color palette | 0-58 |
| `--brightness` | LED brightness | 0.0-1.0 |
| `--num` | Number of LEDs | any |
| `--pin` | GPIO pin | D18, D10, etc. |

## Using Different Palettes

Show all palettes:
```bash
python3 wled_controller.py --list-palettes
```

Try some palettes:
```bash
# Fire palette
python3 wled_controller.py --effect 8 --palette 22

# Aurora palette
python3 wled_controller.py --effect 8 --palette 37

# Ocean palette
python3 wled_controller.py --effect 10 --palette 2
```

## Troubleshooting

### Permission Denied
If you get "Permission denied" errors, run with sudo:
```bash
sudo python3 wled_controller.py --effect 8
```

### No module named 'board'
Install the requirements:
```bash
pip3 install -r requirements.txt
```

### Wrong Colors
Try different pixel orders:
```bash
python3 wled_controller.py --effect 8 --order RGB
python3 wled_controller.py --effect 8 --order GRB
```

### LEDs Not Bright Enough
Increase brightness:
```bash
python3 wled_controller.py --effect 8 --brightness 0.8
```

## Examples

Run the interactive examples:
```bash
python3 example.py
```

Choose from:
1. Rainbow (like your original fx009)
2. Cycle through multiple effects
3. Custom colors demo

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the `effects/` folder to see effect implementations
- Check out `utils/palettes.py` to see all palette definitions
- Modify effects or create your own!

## Quick Reference

**Your original rainbow command** can now be:
```bash
python3 wled_controller.py --effect 8 --speed 20 --num 60 --brightness 0.35 --pin D18
```

Or use the simplified version (most are defaults):
```bash
python3 wled_controller.py --effect 8 --speed 20
```
