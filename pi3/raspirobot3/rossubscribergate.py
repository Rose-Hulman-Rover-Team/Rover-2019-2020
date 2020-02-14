import time
import rospy
#import geometry_msgs.msg
import ar_track_alvar_msgs
#from geometry_msgs.msg import Pose
from ar_track_alvar_msgs.msg import AlvarMarker
#from AlvarMarker import Pose
from rrb3 import *



def callback(msg):
    global rr
    global counter
    global finalForwardCounter
    
    markers = msg.markers
    toterror = 0
    preverror = 0
    xpostotal = 0
    
    #print(disctog)
    if len(markers)> 1:
        
        #print([marker.pose.pose.position.x for marker in markers])
        for marker in markers:
            finalForwardCounter = 0 #resets finalForwardCounter so that the program does not need to be restarted to run multiple times. Stops problem of robot stopping early when    
            #print(marker.pose.pose.position.x)
            xpostotal = xpostotal + marker.pose.pose.position.x
            
        xposavg = xpostotal/len(markers)
        xpostotal = 0;
        #disctog = 0
        
        #marker = markers[0]
        #error  = marker.pose.pose.position.x
        
        error = xposavg
        toterror = error + toterror #total error value for intergal control
        derror = error - preverror #change in error value for derivative control
        
        preverror = error

        kPL = .42 #.4
        kDL = .31 #.3
        kIL = .22

        lspeed = .65 - kPL*error - kDL*derror - kIL*toterror;
        rspeed = .725 + kPL*error + kDL*derror + kIL*toterror; #first sign was negative
        counter = counter + 1
        print("LSPEED: ", lspeed)
        print("RSPEED: ", rspeed)
        print("COUNTER: ", counter)
        #print("Left Speed: ", lspeed)
        #print("Right Speed: ", rspeed)
        print("ERROR: ",error)
        #print(len(markers))

        rr.set_motors(rspeed, 0, lspeed, 0)



        
        
    elif len(markers) <= 1 and counter > 30:
        rr.set_motors(.725, 0, .6, 0)
        finalForwardCounter = finalForwardCounter + 1
        print("finalForwardCounter: ", finalForwardCounter)
        if (finalForwardCounter > 30):
            rr.set_motors(0,0,0,0)
            
            
    else:
        rr.set_motors(0,0,0,0) #this else statement is for in case the robot sees two tags but then loses them and begins to turn in a circle
            
        
        

    #else: 
     #   start_time = time.time()
     #   elapsed_time = time.time() - start_time
        
     #   if counter < 1:
            
            #while elapsed_time > -5 and len(markers) <= 1: #length of time the robot moves forward after it can't see both tags
            #    rr.set_motors(.5, 0, .5, 0)
            #    elapsed_time = start_time - time.time()
            #    print(elapsed_time)
            
       # rr.set_motors(0,0,0,0)
       # print("STOP")
       # counter = counter + 1
        
    rate = rospy.Rate(10) # 10hz
    rate.sleep()
    
def listener():
    rospy.init_node('rossubscriber')
    rospy.Subscriber('ar_pose_marker',  ar_track_alvar_msgs.msg.AlvarMarkers, callback)
   
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

#Area that runs the code

def main():
    disctog = 1
    listener()
    
    
counter = 0
finalForwardCounter = 0
rr = RRB3(9.0, 6.0)
main()