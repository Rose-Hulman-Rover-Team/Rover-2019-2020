# 01_blink3.py
# This program blinks both LEDs on and off rapidly  

import time
from rrb3 import *

rr = RRB3()

print("Press CTRL-c to quit the program")

while True:
    rr.set_led1(1)
    rr.set_led2(1)
    time.sleep(0.1)
    rr.set_led1(0)
    rr.set_led2(0)
    time.sleep(0.1)
