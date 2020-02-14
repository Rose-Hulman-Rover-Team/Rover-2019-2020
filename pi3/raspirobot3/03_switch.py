# 03_switch.py
# If switch is pressed, both LEDs will toggle on and off.

from rrb3 import *
import time

rr = RRB3()

led_on = False

print("Press CTRL-c to quit the program")

while True:
    if rr.sw1_closed():
        led_on = not led_on
        rr.set_led1(led_on)
        rr.set_led2(led_on)    
        time.sleep(0.3)
