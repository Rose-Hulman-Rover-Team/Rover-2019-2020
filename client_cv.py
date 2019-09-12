import base64
import cv2
import zmq

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://192.168.1.99:5555')

camera = cv2.VideoCapture(0)  

while True:
    try:
        grabbed, frame = camera.read()  
        frame = cv2.resize(frame, (224, 224))  
        encoded, buffer = cv2.imencode('.png', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break
