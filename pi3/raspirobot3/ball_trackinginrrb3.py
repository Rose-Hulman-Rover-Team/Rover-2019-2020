# import the necessary packages
from collections import deque
import imutils
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from rrb3 import *

import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32

rr = RRB3(9.0, 6.0)

time.sleep(0.1) #Lets camera get ready
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (28, 86, 6)
greenUpper = (79, 255, 255)
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
        vs = PiRGBArray(camera, size=(640, 480))
        print('Using video feed')
    
 
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
 
# allow the camera or video file to warm up
time.sleep(2.0)
# keep looping
#while True:

xpos = []
ypos = []
timelist = []
xvel = []
yvel = []
xprojpos = [0]
yprojpos = [0]
counter = 0
projcounter = 0
velcounter = 0
t = 1
kill = 0
for frame in camera.capture_continuous(vs, format="bgr", use_video_port=True):
	vs.truncate(0)
	# grab the current frame
	
	# handle the frame from VideoCapture or VideoStream
	#frame = frame[1] if args.get("video", False) else frame
	image = frame.array
	
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
	    break
        
        
	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(image, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		xpos.append(int(x))
		#print("Printing x")
		
		ypos.append(int(y))
		#print("Printing y")
		#print(int(y))
		
		timelist.append(time.time())
		
		#xpos/ypos has one more value than xvel/yvel
	                        
        
                 
		# only proceed if the radius meets a minimum size
		
                    
		if radius > 25:      
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(image, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(image, center, 5, (0, 0, 255), -1)
			print("radius:",radius)
			F=339.58
			D=(2.7*F)/radius
			print("distance:",D)
			
			if D < 8:
                            rr.stop()
			if D > 8:                          #Moves forward if it detects the ball
                            print("Moving FORWARD")
                            rr.forward(0, .6)
                            print(D)
                
                        
                
                            
                       
                            
    	# update the points queue
	pts.appendleft(center)
	
	
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thicknesstwo = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thicknesstwo)
 
	# show the frame to our screen
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
	
	if key == ord("p"):
		print(xpos)
		print(ypos)
		break
	xvel = []
	yvel = []
	    
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
 
# otherwise, release the camera
else:
	vs.release()
 
# close all windows
cv2.destroyAllWindows()
