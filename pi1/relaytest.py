import RPi.GPIO as GPIO
import time
outpin = 11
inpin = 13
GPIO.setwarnings(False) 
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(outpin,GPIO.OUT)
    GPIO.setup(inpin,GPIO.OUT)


    
    
def blink():
    while True:
        GPIO.output(outpin,GPIO.HIGH)
        GPIO.output(inpin,GPIO.LOW)

        time.sleep(10)
        GPIO.output(outpin,GPIO.LOW)
        GPIO.output(inpin,GPIO.HIGH)
        time.sleep(10)

        #GPIO.output(outpin,GPIO.HIGH)
        #GPIO.output(inpin,GPIO.HIGH)
        #time.sleep(2)

        #GPIO.output(outpin,GPIO.LOW)
        #GPIO.output(inpin,GPIO.LOW)

        #time.sleep(2)

def destroy():
    GPIO.output(outpin, GPIO.LOW)
    GPIO.output(inpin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        blink()
    except KeyboardInterrupt:
        destroy()   
