import os
import time
import neopixel
import board

class LEDScontrol:
    def __init__(self, num_pixels, brightness=1.0, auto_write=False, pin=board.D18):
        self.num_pixels = num_pixels
        self.strip = neopixel.NeoPixel(
            pin,
            num_pixels,
            brightness=brightness,
            auto_write=auto_write,
            pixel_order=neopixel.GRB  # WS2812B uses GRB
        )

    def set_pixel(self, index, color):
        """Set a single pixel color. Color is (R, G, B) tuple."""
        if 0 <= index < self.num_pixels:
            self.strip[index] = color

    def fill(self, color):
        """Fill the entire strip with one color."""
        self.strip.fill(color)

    def clear(self):
        """Turn off all the LEDs."""
        self.strip.fill((0, 0, 0))

    def show(self):
        """Update the strip with the new colors."""
        self.strip.show()

    def set_brightness(self, brightness):
        """Set global brightness (0.0 to 1.0)."""
        self.strip.brightness = brightness