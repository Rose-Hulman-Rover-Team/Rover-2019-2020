#!/usr/bin/python 
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
import socket #import socket module
import time,threading
import serial, string
import time

output = " "
lon=0
lat=0
stringVal=""
ser = serial.Serial('/dev/ttyUSB0',115200, 8, 'N',1, timeout = 1)

#defaultdic = copy.deepcopy(dic)

pwm = Adafruit_PCA9685.PCA9685()

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(50)


def send(send):
    
    while(True):
        start =time.time()

        output = (ser.readline().decode())
            
        if output[:6] == "$GPGGA":
            output = output[6:]
        else:
            output ="";
        
             
        send.send((output).encode())

def receive(clientside,dicR):
    
    while(True):
      #  print("thingy")
        
        data = clientside.recv(1024).decode()
        
        data = data.split(",")
        for pair in data:
            item = pair.split(":")
            if(len(item) == 3 and (item[0] in dicR)):
                if(item[2] == "b"):
                    cast = bool 
                    if(item[1] == "0"):
                        item[1] = False
                    else:
                        item[1] = True
                elif(item[2]=="i"):
                    cast = int
                elif(item[2] == "f"):
                    cast = float
                else:
                    cast = str
                 #print("Item[0]:" + item[0] + "Item
                dicR[item[0]] = cast(item[1])
            else:
               o=0;
               #print("\nERROR " + pair + "\n")
            #print(defaultdic)
        if(not dicR["connected"]):
            #print("Controller Disconnected!")
            dicR = {
                "connected": False,
                "BTN_SOUTH": False,
                "BTN_WEST":  False,
                "BTN_NORTH": False,
                "BTN_EAST": False,
                "BTN_START": False,
                "BTN_SELECT": False,
                "BTN_TL": False,
                "BTN_TR": False,
                "BTN_THUMBL": False,
                "BTN_THUMBR": False,
                "ABS_X": 0,
                "ABS_Y": 0,
                "ABS_RX": 0,
                "ABS_RY": 0,
                "ABS_HAT0X": 0,
                "ABS_HAT0Y": 0,
                "ABS_Z": 0,
                "ABS_RZ": 0
            }
        
dic = {
    "connected": False,
    "BTN_SOUTH": False,
    "BTN_WEST":  False,
    "BTN_NORTH": False,
    "BTN_EAST": False,
    "BTN_START": False,
    "BTN_SELECT": False,
    "BTN_TL": False,
    "BTN_TR": False,
    "BTN_THUMBL": False,
    "BTN_THUMBR": False,
    "ABS_X": 0,
    "ABS_Y": 0,
    "ABS_RX": 0,
    "ABS_RY": 0,
    "ABS_HAT0X": 0,
    "ABS_HAT0Y": 0,
    "ABS_Z": 0,
    "ABS_RZ": 0
}



cs = socket.socket() #create a socket object
cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '192.168.1.88' #Host i.p
cport = 12397 #Reserve a port for your service
print ("Start")
cs.connect((host,cport))
print("Laptop -> Pi Connected")

ss = socket.socket() #create a socket object
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sport = 12396 # Reserve a port for your service
ss.bind(('', sport)) #Bind to the port

ss.listen(5) #Wait for the client connection
c,addr = ss.accept() #Establish a connection
print("Pi -> Laptop Connected")
tot = time.time()
sumTime = 0

sendThread = threading.Thread(target=send,args=(c,))
receiveThread = threading.Thread(target=receive,args=(cs,dic,))

sendThread.start()
receiveThread.start()

while(True):
        
        outputL = (dic["ABS_Y"] + 32767) * (450 - 210) // (32767 * 2) + 210
        outputR = (dic["ABS_RY"] + 32767) * (450 - 210) // (32767 * 2) + 210
        outputR = 240 - (outputR - 210) + 210
        print("Left Y:\t\t%.2f\tRight Y:\t%.2f"%((outputL - 330)/120,(outputR - 330)/120))
        if(abs(outputL-330) < 15 ):
                outputL = 330
        if(abs(outputR-330) < 15 ):
                outputR = 330
        pwm.set_pwm(1,0,outputL)
        pwm.set_pwm(0,0,outputR)



    
