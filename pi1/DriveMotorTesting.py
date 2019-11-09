# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


#
#sudo apt-get install git build-essential python-dev
# cd ~
#git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
#cd Adafruit_Python_PCA9685
#

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

mode = 'teleoperated'

pwm.set_pwm_freq(50)

leftChannel = 0
rightChannel = 1

while mode == 'teleoperated':

    #initial input from controller, change later to read an x and a y value
    xvalue = 1026-511
    yvalue = 511-511

    leftVal = yvalue + xvalue + 1023
    rightVal = yvalue - xvalue + 1023

    #Calculated conversion rate: (440-200)/1023
    a = 2046
    convRate = (440-200)/a

    #Use conversion to rate conver 0-1023 to 200-440
    lDriveVal =(int) (leftVal * convRate) + 200
    rDriveVal =(int) (rightVal * convRate) + 200

    #Set the motor controller to calculated speed
    while(True):
        
            pwm.set_pwm(0, 0,330) #runs channel 0 motor
            print("running")
            time.sleep(0.1)

            pwm.set_pwm(1, 0,330)# runs channel 1 motor
            time.sleep(0.1)
##        for i in range(320,190,-1):
##            pwm.set_pwm(leftChannel, 0,500)
##            print(i)
##            time.sleep(0.1)
##    for k in range(320,450):
##        pwm.set_pwm(leftChannel,0,330)
##        print(k)
##        time.sleep(0.1)
    	#pwm.set_pwm(rightChannel, 0, 0)	

    print('Updated value to motor controller',lDriveVal,rDriveVal)

#New middle(stopped) at 330 
#min at 210, max 450

    

