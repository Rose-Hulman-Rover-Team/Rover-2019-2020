
import socket 
#import socket module
#import time
import threading
import cv2
import base64
import numpy as np

def receiveData(client):
	while(True):
		data = client.recv(1024).decode()
		#print(data)


		try:
			frame =  data
			img = base64.b64decode(frame)
			npimg = np.fromstring(img, dtype=np.uint8)
			source = cv2.imdecode(npimg, 1)
			        
			cv2.imshow("Stream", source)
			cv2.waitKey(1)

    	        except KeyboardInterrupt:
			cv2.destroyAllWindows()
        		break


ss = socket.socket() #create a socket object
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


host = '192.168.1.99' #Host i.p
sport = 12397 #Reserve a port for your service
print ("Start")
ss.connect((host,sport))

dic = {}

receiveThread = threading.Thread(target=receiveData, args=(ss,))
receiveThread.start()




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

