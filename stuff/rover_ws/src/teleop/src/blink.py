#!/usr/bin/env python
import rospy
from std_msgs.msg import String

print 'Hello World!'

import RPi.GPIO as gpio
from time import sleep

gpio.setwarnings(False)

gpio.setmode(gpio.BOARD)
gpio.setup(8, gpio.OUT, initial=gpio.LOW)

while True:
        gpio.output(8, gpio.HIGH)
	sleep(1)	
	gpio.output(8, gpio.LOW)
	sleep(1)


