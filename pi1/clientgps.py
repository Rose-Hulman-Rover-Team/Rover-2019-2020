#!/usr/bin/python 

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
               print("\nERROR " + pair + "\n")
            #print(defaultdic)
        if(not dicR["connected"]):
            print("Controller Disconnected!")
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

ss = socket.socket() #create a socket object
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sport = 12396 # Reserve a port for your service
ss.bind(('', sport)) #Bind to the port

ss.listen(5) #Wait for the client connection
c,addr = ss.accept() #Establish a connection
print ("Test")
tot = time.time()
sumTime = 0

sendThread = threading.Thread(target=send,args=(c,))
receiveThread = threading.Thread(target=receive,args=(cs,dic,))

sendThread.start()
receiveThread.start()

#file = open("Save.csv", "w")


##dic = {}
##
##
##for i in range(0,100000):
##    start =time.time()
##
##    output = (ser.readline().decode())
##        
##    if output[:6] == "$GPGGA":
##        output = output[:6]
##    else:
##        output ="";
##    
##    print(output)       
##    c.send((output).encode())
##    
##    data = cs.recv(1024).decode()
##    print(data)
##    data = data.split(",")
##    for pair in data:
##        item = pair.split(":")
##        if(item[2] == "b"):
##            cast = bool
##        elif(item[2]=="i"):
##            cast = int
##        elif(item[2] == "f"):
##            cast = float
##        else:
##            cast = str
##         #print("Item[0]:" + item[0] + "Item  
##        dic[item[0]] = cast(item[1])
##    
##    print(str(dic))
##    #print ((cs.recv(1024)).decode())
##    end = time.time()
##    sumTime = sumTime + (end-start)
##    
##tot = time.time() - tot
##sumTime = sumTime/100.0
##print (tot, '  ',sumTime)
##cs.close


    
