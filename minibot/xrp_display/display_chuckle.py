from XRPLib.defaults import *

import st7789_fb_plus as st7789
from machine import Pin, SPI
import machine
import time
import math

# === Display Setup ===
spi = SPI(0, baudrate=24000000)
display = st7789.ST7789_SPI(spi,
                            240, 320,
                            reset=None,
                            cs=machine.Pin(17, Pin.OUT, value=1),
                            dc=machine.Pin(16, Pin.OUT, value=1),
                            backlight=None,
                            bright=1,
                            rotation=3,
                            color_order=st7789.BGR,
                            reverse_bytes_in_word=True)

# === Crescent Eye Drawing ===
def draw_crescent_eye_up(x, y, xr, yr):
    display.ellipse(x, y, xr, yr, st7789.YELLOW, fill=True)
    display.ellipse(x, y + yr // 3, xr - 3, yr - 3, st7789.BLACK, fill=True)
    display.rect(x + xr // 2, y - yr, 50, 60, color=st7789.BLACK, fill=True)
    display.rect(x - xr - 15, y - yr, 40, 60, color=st7789.BLACK, fill=True)

def draw_eye_pair(center_x, center_y, xr, yr, gap=10):
    left_eye_x = center_x - xr - gap // 2
    right_eye_x = center_x + xr + gap // 2
    draw_crescent_eye_up(left_eye_x, center_y, xr, yr)
    draw_crescent_eye_up(right_eye_x, center_y, xr, yr)

# === Orbit Animation ===
def animate_orbit_and_bounce():
    xr = 60
    yr = 45
    eye_gap = 10

    cx = 160  # center of circular path (horizontal)
    cy = 120  # center of circular path (vertical)
    radius = 30

    # Circle around the screen
    for angle_deg in range(0, 360, 5):
        angle_rad = math.radians(angle_deg)
        x = int(cx + radius * math.cos(angle_rad))
        y = int(cy + radius * math.sin(angle_rad))
        display.fill(st7789.BLACK)
        draw_eye_pair(x, y, xr, yr, gap=eye_gap)
        display.show()
        time.sleep(0.01)

    # Bounce a few times
    bounce_amplitude = 20
    for t in range(20):
        offset = int(bounce_amplitude * math.sin(t * math.pi / 5))
        display.fill(st7789.BLACK)
        draw_eye_pair(cx, cy + offset, xr, yr, gap=eye_gap)
        display.show()
        time.sleep(0.01)

# === Run Animation ===
while True:
    animate_orbit_and_bounce()
