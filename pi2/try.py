import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)
cap.set(3, 160)
cap.set(4, 121)
cap2.set(3,160)
cap2.set(4,121)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2,frame2 = cap2.read()
   # frame = cv2.resize(frame, (512,218))
   # frame2 = cv2.resize(frame2, (512,218))

    vertical = np.concatenate((frame, frame2), axis=0)
    #cv2.imwrite("out.jpg", vertical)
    # Display the resulting frame
    cv2.imshow('frame',vertical)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()