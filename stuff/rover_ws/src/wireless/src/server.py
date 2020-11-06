#!/usr/bin/env python
import socket  #import socket module
import time
import threading
import cv2
import base64

#camera = cv2.VideoCapture(0)

def sendData(client):
	while(True): 
	#grabbed, frame = camera.read()  
        #frame = cv2.resize(frame, (640, 480))  
        #encoded, buffer = cv2.imencode('.jpg', frame)
        #jpg_as_text = base64.b64encode(buffer)
        	str = "hello hello hello hello hello"
       
        #client.send(jpg_as_text.encode())
		client.send(str)
        #time.sleep(0.005)

cs = socket.socket() #create a socket object
cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
cport = 12397 # Reserve a port for your service
cs.bind(('', cport)) #Bind to the port

cs.listen(5) #Wait for the client connection
c,addr = cs.accept() #Establish a connection

sendThread = threading.Thread(target=sendData, args=(c,))
sendThread.start()

cs.close
