import numpy as np
import cv2

from socket import *

cap = cv2.VideoCapture(0)

FPS = cap.get(5)
setFPS = 10
ratio = int(FPS)/setFPS

host = "192.168.1.99"
port = 4096

addr = (host, port)
buf = 1024

def sendFile(fName):
	s = socket(AF_INET, SOCK_DGRAM)
	s.sendto(fName, addr)
	f = open(fName, "rb")
	data = f.read(buf)
	while data:
		if(s.sendto(data, addr)):
			data = f.read(buf)
	f.close()
	s.close()

def captureFunc():
	count = 0
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == True:
			cv2.imshow('frame', frame)
			count = count + 1
			if count == ratio:
				cv2.imwrite("img.jpg", frame)
				sendFile("img.jpg")
				count = 0
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			break

if __name__ == '__main__':
	captureFunc()
	cap.release()
	cv2.destroyAllWindows()
