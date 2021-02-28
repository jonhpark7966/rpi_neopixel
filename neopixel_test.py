# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels

num_pixels = 414

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=ORDER
        )
while True:
    for i in range(144):
        if(i%2) == 0:
            pixels[i] = ((0x05, 0xd9, 0xe8, 0))
        else:
            pixels[i] = ((219, 41, 110, 0))
    for i in range(145, num_pixels):
        pixels[i] = (0,0,0,0)

    pixels.show()

    for i in range(144):
        if(i%2) == 1:
            pixels[i] =((0x05, 0xd9, 0xe8, 0))
        else:
            pixels[i] =  ((219, 41, 110, 0))

    pixels.show()



    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 255, 0, 0))
#    pixels.show()
#    time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
#    pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((0, 0, 255, 0))
#    pixels.show()
#    time.sleep(1)

