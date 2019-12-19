#!/usr/bin/env python

import rospy
import serial
import pynmea2
from std_msgs.msg import String

def calibrate(long,lat):
    x = (float(long)/100) + 0.19429499999999678 # North Calibrator: 0.19429499999999678
    y = (float(lat)/100) + 0.12900099997742132  # West Calibrator: 0.12900099997742132
    return (x,-y)

def talker():
    pub = rospy.Publisher('gps', String, queue_size=10)
    rospy.init_node('gps_talker', anonymous=True)
    rate = rospy.Rate(10)

    port = '/dev/ttyUSB0'

    ser = serial.Serial(port, 115200, 8, 'N',1, timeout=1)
    for i in range(10):
        ser.readline()

    while not rospy.is_shutdown():
        output = ser.readline().decode('ascii', errors='replace')
        if  output[:6] == '$GPGGA' :
            nmeaobj = pynmea2.parse(output)

            coord = (nmeaobj.data[1], nmeaobj.data[3])
            
            if not isinstance(coord[0], str) and not isinstance(coord[1], str):
                coord = calibrate(coord[0], coord[1])
            x,y = coord

            hello_str = "coordinates: {} N, {} W"  
            message = hello_str.format(coord[0], coord[1])

            rospy.loginfo(message)
            pub.publish(message)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass