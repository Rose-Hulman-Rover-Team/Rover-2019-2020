#!/usr/bin/python 
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
import socket #import socket module
import time,threading
import serial, string
import time


pwm = Adafruit_PCA9685.PCA9685()

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)



while(True):
        
        outputL = 440#(dic["ABS_Y"] + 32767) * (450 - 210) // (32767 * 2) + 210
        outputR = 440#(dic["ABS_RY"] + 32767) * (450 - 210) // (32767 * 2) + 210
        outputR = 240 - (outputR - 210) + 210
        print("Left Y:\t\t%.2f\tRight Y:\t%.2f"%((outputL - 330)/120,(outputR - 330)/120))
        if(abs(outputL-330) < 15 ):
                outputL = 330
        if(abs(outputR-330) < 15 ):
                outputR = 330
        pwm.set_pwm(1,0,outputL)
        pwm.set_pwm(0,0,outputR)



    
