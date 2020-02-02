import pynmea2, serial, os, time, sys, glob, datetime

import rospy
from std_msgs.msg import String
   
def talker(message):
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(message)
        pub.publish(message)
        rate.sleep() 


def logfilename():
    now = datetime.datetime.now()
    return 'GPGGA_NMEA_%0.4d-%0.2d-%0.2d_%0.2d-%0.2d-%0.2d.nmea' % \
                (now.year, now.month, now.day,
                 now.hour, now.minute, now.second)

def adjustment(long,lat):
    x = (float(long)/100) + 0.19429499999999678 # 0.19429499999999678
    y = (float(lat)/100) + 0.12900099997742132  # 0.12900099997742132
    return (x,-y)

output = " "
lon=0
lat=0
stringVal=""
port = '/dev/ttyUSB0'

outfname = logfilename()
sys.stderr.write('Logging data on %s to %s\n' % (port, outfname))
f = open(outfname, 'wb')
    
with serial.Serial(port, 115200, 8, 'N',1, timeout=1) as ser:
    for i in range(10):
        ser.readline()

    while True:
        output = ser.readline().decode('ascii', errors='replace')
        if  output[:6] == '$GPGGA' :
            nmeaobj = pynmea2.parse(output)
            fileds = []

            coord = (nmeaobj.data[1], nmeaobj.data[3])

            if isinstance(coord[0], str) and isinstance(coord[1], str):
                coord = adjustment(coord[0], coord[1])

            for i in range(len(nmeaobj.fields)):
                if i == 1:
                    data = coord[0]
                elif i == 3:
                    data = coord[1]
                else:
                    data = nmeaobj.data[i]
                filed = (nmeaobj.fields[i][0], data)
                fileds.append(filed)

            print("")
            print("GPS Type: " + output[:6])
            print("Update GPS Data Point")
            for filed in fileds:
                print("%s:  %s" % (filed[0], filed[1]))
               
            print("")
            print("")
            
            f.write(output)
            f.write("\n")
f.close()


# ---------------------------------------------------------------------------------------------
#ser = serial.Serial('/dev/ttyUSB0',115200, 8, 'N',1, timeout = 1)
#file = open("Save.csv", "w")

"""
while True:
    print("----")
    
    while output != "":
        output = (ser.readline().decode())
        
        if output[:6] == "$GPGGA":
            ##`output=output.split(",")[2:6];
           
##            stringVal=output[0]
##            lat=float(stringVal[:2])+float(stringVal[2:])/60
##            stringVal=output[2]
##            lon=float(stringVal[:3])+float(stringVal[3:])/60
##            print("Latitude:\t" + str(lat) + "\tLongitude:\t" + str(lon))
            print(output)
        #file.write(output.decode("utf-8"))
        
    output =" "
    """

##Pervious one that worked on old pi

##import serial, string
##import time 
##output = " "
##lon=0
##lat=0
##stringVal=""
##ser = serial.Serial('/dev/ttyUSB0',115200, 8, 'N', 1, timeout = 1)
###file = open("Save.csv", "w")
##while True:
##    print("----")
##    while output != "":
##        output = (ser.readline())
##        print(output)
####        if output[:6] == "$GPGGA":
####            output=output.split(",")[2:6];
####            stringVal=output[0]
####            lat=float(stringVal[:2])+float(stringVal[2:])/60
####            stringVal=output[2]
####            lon=float(stringVal[:3])+float(stringVal[3:])/60
####            print("Latitude:\t" + str(lat) + "\tLongitude:\t" + str(lon))
##        #file.write(output.decode("utf-8"))
##        
##    output =" "
##
##
##file.close()
##
##