#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'heard')

def listener():
    rospy.init_node('gps_listener', anonymous=True)

    rospy.Subscriber('gps', String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
