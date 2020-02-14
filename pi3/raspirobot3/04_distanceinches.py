# 04_distance.py
# Uses the ultrasonic rangefinder to measure distance

from rrb3 import *
import time

rr = RRB3()

print("Press CTRL-c to quit the program")

while True:
    dist = rr.get_distance() / 2.5 #converts the distance from cm to in
    print(dist)
    time.sleep(0.5)
