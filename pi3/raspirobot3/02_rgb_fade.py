# 02_rgb_fade.py
# Turn on the RGB LED colours for 1 second each

from squid import *
import time

squid = Squid(18, 23, 24)

try:
    while True:
        for i in range(0, 100):
            squid.set_color((i, 0, 0))
            time.sleep(0.05)
        
finally: 
    GPIO.cleanup()
