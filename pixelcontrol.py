import time
import board
import neopixel


class PixelControl:

    def __init__(self):
        self.num_pixels = 16
#        self.pixel_pin = board.D12
        self.pixel_pin = board.D18
        self.order = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.order
        )

    def red(self):
        self.pixels.fill((255, 0, 0))
        self.pixels.show()

    def green(self):
        self.pixels.fill((0, 255, 0))
        self.pixels.show()

    def blue(self):
        self.pixels.fill((0, 0, 255))
        self.pixels.show()

    def fill(self, vals):
        self.pixels.fill(vals)
        self.pixels.show()

    def off(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def _get_rainbow_color(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self._get_rainbow_color(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def rainbow(self):
        self.rainbow_cycle(0.01)

