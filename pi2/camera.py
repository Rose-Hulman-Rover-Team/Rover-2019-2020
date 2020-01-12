import socket
import cv2
import sys
from threading import Thread, Lock
import sys
import numpy as np

debug = True
jpeg_quality = 10
host = "192.168.1.77"
port = 1080

class VideoGrabber(Thread):
        """A threaded video grabber.
        
        Attributes:
        encode_params (): 
        cap (str): 
        attr2 (:obj:`int`, optional): Description of `attr2`.
        
        """
        def __init__(self, jpeg_quality):
            Thread.__init__(self)
            self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
            self.cap1= cv2.VideoCapture(0)
            self.cap2= cv2.VideoCapture(2)
            self.running = True
            self.buffer = None
            self.lock = Lock()

        def stop(self):
            self.running = False

        def get_buffer(self):
            """Method to access the encoded buffer.
               Returns:
               np.ndarray: the compressed image if one has been acquired. None otherwise.
            """
            if self.buffer is not None:
                self.lock.acquire()
                cpy = self.buffer.copy()
                self.lock.release()
                return cpy
                
        def run(self):
            while self.running:
                success1, img1 = self.cap1.read()
                success2, img2 = self.cap2.read()
                if not success1:
                    continue
                    
                img1 = cv2.resize(img1, (512,218))
                img2 = cv2.resize(img2, (512,218))
                vertical = np.concatenate((img1, img2), axis=0)
		#cv2.imwrite("vertical.jpg", img1)
                # JPEG compression
                # Protected by a lock
                # As the main thread may asks to access the buffer
                self.lock.acquire()
                result, self.buffer = cv2.imencode('.jpg', img1, self.encode_param)
                self.lock.release()


grabber = VideoGrabber(jpeg_quality)
grabber.start()

running = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = (host, port)

print('starting up on %s port %s\n' % server_address)

sock.bind(server_address)

while(running):
        data, address = sock.recvfrom(4)
        if(data == "get"):
                buffer = grabber.get_buffer()
                if buffer is None:
                        continue
                if len(buffer) > 65507:
                        print("The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
                        sock.sendto("FAIL",address)
                        continue
                # We sent back the buffer to the client
                sock.sendto(buffer.tobytes(), address)
        elif(data == "quit"):
                grabber.stop()
                running = False
        
print("Quitting..")
grabber.join()
sock.close()
