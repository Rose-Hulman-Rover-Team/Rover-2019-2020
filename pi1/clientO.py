#!/usr/bin/python 

import socket #import socket module

s = socket.socket() #create a socket object
host = '192.168.1.70' #Host i.p
port = 12397 #Reserve a port for your service

s.connect((host,port))
print s.recv(1024)
s.close
