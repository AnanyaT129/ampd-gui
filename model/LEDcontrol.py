from enum import Enum
import os
import time
import neopixel
import board

class LEDStatus(Enum):
    OFF = (0, 0, 0)
    READY = (255, 0, 0)
    RUNNING = (255, 255, 0)
    ERROR = (0, 255, 0)

    PLASTIC_DETECTED = (0, 255, 0)
    PLASTIC_NOT_DETECTED = (255, 0, 0)
    PLASTIC_CONTENT_UNSURE = (255, 255, 0)

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
    
    def set_lighting(self, status: LEDStatus):
        match(status):
            # status of the device turns first light on
            case LEDStatus.OFF | LEDStatus.READY | LEDStatus.RUNNING | LEDStatus.ERROR:
                print(status.value)
                self.clear()
                self.set_pixel(0, status.value)
            
            # plastic result turns everything but the first light on
            case LEDStatus.PLASTIC_DETECTED | LEDStatus.PLASTIC_NOT_DETECTED | LEDStatus.PLASTIC_CONTENT_UNSURE:
                print(status.value)
                self.clear()
                self.fill(status.value)
                self.set_pixel(0, (0, 0, 0))
        
        self.show()