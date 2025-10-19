#!/usr/bin/env python3
"""
Example usage of WLED effects library
Demonstrates how to use the library programmatically
"""
import time
import board
import neopixel
from segment import Segment
from effects.basic_effects import (
    mode_rainbow_cycle,
    mode_theater_chase,
    mode_twinkle,
    mode_running_lights,
    get_effect
)
from utils.colors import rgb_to_color

def example_rainbow():
    """Example: Rainbow effect (your original fx009)"""
    print("Running Rainbow Cycle effect...")

    # Setup hardware
    pixels = neopixel.NeoPixel(
        board.D18, 60,
        brightness=0.35,
        auto_write=False,
        pixel_order=neopixel.GRB
    )

    # Create segment
    segment = Segment(pixels, 0, 60)
    segment.speed = 20  # Matching your original example

    # Run effect
    try:
        while True:
            delay_ms = mode_rainbow_cycle(segment)
            segment.call += 1
            pixels.show()
            time.sleep(delay_ms / 1000.0)
    except KeyboardInterrupt:
        pixels.fill((0, 0, 0))
        pixels.show()
        print("\nStopped!")

def example_cycle_effects():
    """Example: Cycle through multiple effects"""
    print("Cycling through effects...")

    pixels = neopixel.NeoPixel(
        board.D18, 60,
        brightness=0.35,
        auto_write=False,
        pixel_order=neopixel.GRB
    )

    segment = Segment(pixels, 0, 60)

    # List of effects to cycle through
    effects = [
        (8, "Rainbow Cycle", 10),      # ID, name, duration in seconds
        (9, "Theater Chase", 10),
        (13, "Twinkle", 10),
        (10, "Running Lights", 10),
    ]

    try:
        for effect_id, effect_name, duration in effects:
            print(f"\nRunning: {effect_name}")
            segment.reset()
            effect_func = get_effect(effect_id)

            start_time = time.time()
            while time.time() - start_time < duration:
                delay_ms = effect_func(segment)
                segment.call += 1
                pixels.show()
                time.sleep(delay_ms / 1000.0)

    except KeyboardInterrupt:
        pass
    finally:
        pixels.fill((0, 0, 0))
        pixels.show()
        print("\nStopped!")

def example_custom_colors():
    """Example: Using custom colors"""
    print("Running with custom colors...")

    pixels = neopixel.NeoPixel(
        board.D18, 60,
        brightness=0.35,
        auto_write=False,
        pixel_order=neopixel.GRB
    )

    segment = Segment(pixels, 0, 60)

    # Set custom colors
    segment.colors[0] = rgb_to_color(255, 0, 255)    # Magenta
    segment.colors[1] = rgb_to_color(0, 255, 255)    # Cyan
    segment.colors[2] = rgb_to_color(255, 255, 0)    # Yellow

    # Run blink effect with custom colors
    from effects.basic_effects import mode_blink

    try:
        while True:
            delay_ms = mode_blink(segment)
            segment.call += 1
            pixels.show()
            time.sleep(delay_ms / 1000.0)
    except KeyboardInterrupt:
        pixels.fill((0, 0, 0))
        pixels.show()
        print("\nStopped!")

if __name__ == "__main__":
    import sys

    examples = {
        "1": ("Rainbow (like your original fx009)", example_rainbow),
        "2": ("Cycle through effects", example_cycle_effects),
        "3": ("Custom colors", example_custom_colors),
    }

    print("\nWLED Examples")
    print("=" * 50)
    for key, (desc, _) in examples.items():
        print(f"{key}. {desc}")
    print()

    choice = input("Choose example (1-3) [1]: ").strip() or "1"

    if choice in examples:
        examples[choice][1]()
    else:
        print("Invalid choice!")
