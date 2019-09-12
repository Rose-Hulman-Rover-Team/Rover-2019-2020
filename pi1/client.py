#!/usr/bin/python 

import socket #import socket module
import time
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

dic = {}
for i in range(0,100000):
    start =time.time()
    c.send(("a"*10  + "z").encode())
    data = cs.recv(1024).decode()
    print(data)
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
    #print ((cs.recv(1024)).decode())
    end = time.time()
    sumTime = sumTime + (end-start)
    
tot = time.time() - tot
sumTime = sumTime/100.0
print (tot, '  ',sumTime)
cs.close
