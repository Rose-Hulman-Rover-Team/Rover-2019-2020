#!/usr/bin/python

import socket #import the socket module

s = socket.socket() #Create a socket object
port = 12397 # Reserve a port for your service
s.bind(('',port)) #Bind to the port

s.listen(5) #Wait for the client connection
i=0
while i<5000:
    c,addr = s.accept() #Establish a connection with the client
    print "Got connection from", addr
    c.send("Thank you for connecting!")
    i=i+1

c.close()
