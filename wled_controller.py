#!/usr/bin/env python3
"""
WLED Controller for Raspberry Pi
Main controller for running WLED effects on NeoPixel strips
"""
import time
import argparse
import board
import neopixel
from segment import Segment
from effects.basic_effects import get_effect, get_all_effects, FRAMETIME
from utils.palettes import PALETTE_NAMES

class WLEDController:
    """Main WLED controller"""

    def __init__(self, num_leds: int, pin, brightness: float = 0.35,
                 pixel_order=neopixel.GRB):
        """
        Initialize WLED controller
        num_leds: number of LEDs in strip
        pin: board pin (e.g., board.D18)
        brightness: 0.0-1.0
        pixel_order: neopixel color order
        """
        self.num_leds = num_leds
        self.pixels = neopixel.NeoPixel(
            pin, num_leds,
            brightness=brightness,
            auto_write=False,
            pixel_order=pixel_order
        )

        # Create main segment (entire strip)
        self.segment = Segment(self.pixels, 0, num_leds)

        # Current effect
        self.current_effect = 9  # Default to Rainbow Cycle (fx009)
        self.running = False

    def set_effect(self, effect_id: int):
        """Set current effect"""
        self.current_effect = effect_id
        self.segment.reset()

    def set_speed(self, speed: int):
        """Set effect speed (0-255)"""
        self.segment.speed = max(0, min(255, speed))

    def set_intensity(self, intensity: int):
        """Set effect intensity (0-255)"""
        self.segment.intensity = max(0, min(255, intensity))

    def set_palette(self, palette_id: int):
        """Set color palette (0-58)"""
        self.segment.palette_id = max(0, min(58, palette_id))

    def set_colors(self, color1: int = None, color2: int = None, color3: int = None):
        """Set segment colors"""
        if color1 is not None:
            self.segment.colors[0] = color1
        if color2 is not None:
            self.segment.colors[1] = color2
        if color3 is not None:
            self.segment.colors[2] = color3

    def set_brightness(self, brightness: float):
        """Set global brightness (0.0-1.0)"""
        self.pixels.brightness = max(0.0, min(1.0, brightness))

    def run(self):
        """Run the effect loop"""
        self.running = True
        effect_func = get_effect(self.current_effect)

        try:
            while self.running:
                # Call effect function
                delay_ms = effect_func(self.segment)
                self.segment.call += 1

                # Update strip
                self.pixels.show()

                # Delay
                time.sleep(delay_ms / 1000.0)

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop and clear the strip"""
        self.running = False
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def list_effects(self):
        """Print all available effects"""
        print("\nAvailable Effects:")
        print("-" * 40)
        for effect_id, name in get_all_effects():
            marker = " <--" if effect_id == self.current_effect else ""
            print(f"  {effect_id:3d}: {name}{marker}")
        print()

    def list_palettes(self):
        """Print all available palettes"""
        print("\nAvailable Palettes:")
        print("-" * 40)
        for i, name in enumerate(PALETTE_NAMES):
            marker = " <--" if i == self.segment.palette_id else ""
            print(f"  {i:2d}: {name}{marker}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="WLED Controller for Raspberry Pi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run rainbow effect (default)
  python3 wled_controller.py

  # Run specific effect with custom speed
  python3 wled_controller.py --effect 1 --speed 200

  # Use specific palette
  python3 wled_controller.py --effect 8 --palette 22

  # List all effects
  python3 wled_controller.py --list-effects

  # List all palettes
  python3 wled_controller.py --list-palettes
        """
    )

    parser.add_argument("--num", type=int, default=60,
                       help="Number of LEDs (default: 60)")
    parser.add_argument("--brightness", type=float, default=0.35,
                       help="Brightness 0.0-1.0 (default: 0.35)")
    parser.add_argument("--effect", "-e", type=int, default=8,
                       help="Effect ID (default: 8 = Rainbow Cycle)")
    parser.add_argument("--speed", "-s", type=int, default=128,
                       help="Effect speed 0-255 (default: 128)")
    parser.add_argument("--intensity", "-i", type=int, default=128,
                       help="Effect intensity 0-255 (default: 128)")
    parser.add_argument("--palette", "-p", type=int, default=0,
                       help="Palette ID 0-58 (default: 0)")
    parser.add_argument("--order", choices=["GRB", "RGB", "RGBW", "GRBW"],
                       default="GRB",
                       help="Pixel color order (default: GRB)")
    parser.add_argument("--pin", default="D18",
                       help="Board pin, e.g. D18 is GPIO18 (default: D18)")
    parser.add_argument("--list-effects", action="store_true",
                       help="List all available effects and exit")
    parser.add_argument("--list-palettes", action="store_true",
                       help="List all available palettes and exit")

    args = parser.parse_args()

    # Map pixel order
    order_map = {
        "GRB": neopixel.GRB,
        "RGB": neopixel.RGB,
        "RGBW": neopixel.RGBW,
        "GRBW": neopixel.GRBW
    }
    pixel_order = order_map[args.order]

    # Get pin
    pin = getattr(board, args.pin)

    # Create controller
    controller = WLEDController(
        args.num,
        pin,
        brightness=args.brightness,
        pixel_order=pixel_order
    )

    # Handle list commands
    if args.list_effects:
        controller.list_effects()
        return

    if args.list_palettes:
        controller.list_palettes()
        return

    # Configure and run
    controller.set_effect(args.effect)
    controller.set_speed(args.speed)
    controller.set_intensity(args.intensity)
    controller.set_palette(args.palette)

    print(f"\nWLED Controller for Raspberry Pi")
    print(f"=" * 50)
    print(f"LEDs:       {args.num}")
    print(f"Brightness: {args.brightness}")
    print(f"Effect:     {args.effect} ({get_all_effects()[args.effect][1] if args.effect < len(get_all_effects()) else 'Unknown'})")
    print(f"Speed:      {args.speed}")
    print(f"Intensity:  {args.intensity}")
    print(f"Palette:    {args.palette} ({PALETTE_NAMES[args.palette] if args.palette < len(PALETTE_NAMES) else 'Unknown'})")
    print(f"Pin:        {args.pin}")
    print(f"\nPress Ctrl+C to stop")
    print("=" * 50 + "\n")

    controller.run()

if __name__ == "__main__":
    main()
