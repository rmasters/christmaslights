import random
import time

import board
import adafruit_ws2801 as pixels

odata = board.MOSI
oclock = board.SCK

def random_colour():
    return random.randrange(0, 7) * 32

leds = pixels.WS2801(oclock, odata, 25, brightness=1.0, auto_write=True)
while True:
    for idx in range(len(leds)):
        leds[idx] = (random_colour(), random_colour(), random_colour())
        time.sleep(.15)

