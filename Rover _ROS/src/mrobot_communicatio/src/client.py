import socket #import socket module
import time
import inputs
import threading
import asyncore
import logging
import json


def receiveData(client):
    while(True):
        data = client.recv(1024).decode()
        #print(data)

def sendData(client):
    while(True):
        try:
            events = inputs.get_gamepad()
            sendString = "connected:1:b,"
            for event in events:
                if(event.ev_type == "Absolute"):
                    sendString += event.code + ":" + str(event.state) + ":i,"
                elif(event.ev_type == "Key"):
                    sendString += event.code + ":" + str(event.state) + ":b,"
        except inputs.UnpluggedError:
            sendString = "connected:0:b,"
            time.sleep(0.1)

        sendString = sendString[:-1]   #Remove ending ","
        client.send(sendString.encode())
        #time.sleep(0.005)
print("Start")        
ss = socket.socket() #create a socket object
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

cs = socket.socket() #create a socket object
cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cport = 12397 # Reserve a port for your service
cs.bind(('', cport)) #Bind to the port
cs.listen(5) #Wait for the client connection
c,addr = cs.accept() #Establish a connection
print("Laptop -> Pi Connected")

host = '192.168.1.42' #Host i.p
sport = 12396 #Reserve a port for your service
ss.connect((host,sport))
print("Pi -> Laptop Connected")

print ("Test")
tot = time.time()
sumTime = 0

dic = {}

receiveThread = threading.Thread(target=receiveData, args=(ss,))
sendThread = threading.Thread(target=sendData, args=(c,))

receiveThread.start()
sendThread.start()
'''
for i in range(0,100000):
    print("start")
    start=time.time()
    data = ss.recv(1024).decode()
    print("Recieve")

    #print(data)
    data = data.split(",")
    for pair in data:
        item = pair.split(":")
        if(item[2] == "b"):
            cast = bool
        elif(item[2]=="i"):
            cast = int
        elif(item[2] == "f"):
            cast = float
        else:
            cast = str
         #print("Item[0]:" + item[0] + "Item  
        dic[item[0]] = cast(item[1])
    
    print(str(dic))


    print("done")
    end = time.time()
    sumTime = sumTime + (end-start)


    #print ((cs.recv(1024)).decode())

'''
    
tot = time.time() - tot
sumTime = sumTime/100.0
print (tot, '  ',sumTime)
cs.close
