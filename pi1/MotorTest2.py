# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


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

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)

#off 321
#max 410ish
#min 230ish 
print('Moving servo on channel 0, press Ctrl-C to quit...')
#while True:
    # Move servo on channel O between extremes.
    #for x in range(0, 4095):
     #   pwm.set_pwm(1, 0, x)
      #  time.sleep(.001)
    #time.sleep(1)
    #pwm.set_pwm(1, 0, 0)
    #time.sleep(2)
      #pwm.set_pwm(0,0, 410)
      #pwm.set_pwm(1,0, 320)
     #   for k in range(230,410):
     #      pwm.set_pwm(0, 0, k)
    #     time.sleep(.01)
    #       print(k)
##    for j in range(200,410):
##       pwm.set_pwm(0, 0,640-j)
##       time.sleep(.1)
##       print(640-j)
   #pwm.set_pwm(2, 0, 4095)
   #pwm.set_pwm(3, 0, 4095)
   #pwm.set_pwm(4, 0, 4095)
   #pwm.set_pwm(5, 0, 4095)
   #pwm.set_pwm(6, 0, 4095)
   
   #time.sleep(5)
   
    #pwm.set_pwm(0, 0, 311)
   #pwm.set_pwm(2, 0, 0)
   #pwm.set_pwm(3, 0, 0)
   #pwm.set_pwm(4, 0, 0)
   #pwm.set_pwm(5, 0, 0)
   #pwm.set_pwm(6, 0, 0)
   
    #time.sleep(1)
##    time.sleep(1)
##    pwm.set_pwm(1, 0, 4095)
##    time.sleep(1)

