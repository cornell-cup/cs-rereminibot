# Import libraries
import st7789_fb_plus as st7789
from machine import Pin, SPI
import machine

# Create SPI object
spi = SPI(0, baudrate=24000000)

# Create display object
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

# Now we're ready to use the display! All drawing functions fill a
# buffer, which only gets sent to the display when show() is called

# Fill display with a color to create a background color
display.fill(st7789.RED)

# Draw a rectangle
display.rect(x=200, y=50, w=75, h=25, color=st7789.GREEN, fill=False)

# Draw an ellipse
display.ellipse(x=50, y=50, xr=20, yr=40, color=st7789.BLUE, fill=True)

# Draw a polygon
pts = bytearray([0,0,
				100,20,
				0,80,
				100,70])
display.simple_poly(points = pts, x=100, y=100, color=st7789.BLACK, fill=True)

# Draw some text
display.text("Hello world!", 100, 200)

# Now actually send the image to the display
display.show()