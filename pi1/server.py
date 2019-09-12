#!/usr/bin/python

import socket #import the socket module

s = socket.socket() #Create a socket object
host = socket.gethostname() #Get the local machine name
port = 12397 # Reserve a port for your service
s.bind(('', port)) #Bind to the port

s.listen(5) #Wait for the client connection
c,addr = s.accept() #Establish a connection
while True:
    #print i
    c.send("Thank you for connecting!")
    
c.close()
print ("TEST")
