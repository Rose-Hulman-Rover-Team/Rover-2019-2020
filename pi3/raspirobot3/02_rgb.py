# 02_rgb.py
# Turn on the RGB LED colours for 1 second each

from squid import *
import time

squid = Squid(18, 23, 24)

try:
    while True:
        squid.set_color(RED)
        time.sleep(1)
        squid.set_color(GREEN)
        time.sleep(1)
        squid.set_color(BLUE)
        time.sleep(1)
        
finally: 
    GPIO.cleanup()
