import RPi.GPIO as GPIO
import time
ledPinBlue = 11
ledPinYellow = 13
ledPinGreen = 40
ledPinRed = 15
yPin = 29
xPin = 31
GPIO.setwarnings(False) 
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPinBlue,GPIO.OUT)
    GPIO.setup(ledPinYellow,GPIO.OUT)
    GPIO.setup(ledPinRed,GPIO.OUT)
    GPIO.setup(ledPinGreen,GPIO.OUT)
    GPIO.setup(xPin,GPIO.IN)
    GPIO.setup(yPin,GPIO.IN)
    
    
def blink():
    while True:
        y = GPIO.input(yPin)
        x = GPIO.input(xPin)
        GPIO.output(ledPinBlue,GPIO.HIGH)
        GPIO.output(ledPinYellow,GPIO.HIGH)
        GPIO.output(ledPinRed,GPIO.HIGH)
        GPIO.output(ledPinGreen,GPIO.HIGH)
        #keyPress = raw_input("Hit wasd")
        print(x)
        print(y)
#        if(y==1):
#            GPIO.output(ledPinBlue,GPIO.LOW)
#            time.sleep(.1)
#        if(x==0):
#            GPIO.output(ledPinYellow,GPIO.LOW)
#            time.sleep(.1)
#        if(y==0):
#            GPIO.output(ledPinRed,GPIO.LOW)
#            time.sleep(.1)
#        if(x == 1):
#            GPIO.output(ledPinGreen,GPIO.LOW)
#            time.sleep(.1)
        #if(keyPress == "s"):
         #   GPIO.output(ledPinRed,GPIO.LOW)
          #  time.sleep(2)
        #if(keyPress == "d"):
         #   GPIO.output(ledPinGreen,GPIO.LOW)
          #  time.sleep(2)
        
        
        time.sleep(1)
        GPIO.output(ledPinGreen,GPIO.LOW)
	time.sleep(2)
def destroy():
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        blink()
    except KeyboardInterrupt:
        destroy()
