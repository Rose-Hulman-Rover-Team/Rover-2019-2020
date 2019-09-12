
import serial, string
import time 
output = " "
lon=0
lat=0
stringVal=""
ser = serial.Serial('/dev/ttyUSB0',115200, 8, 'N',1, timeout = 1)
#file = open("Save.csv", "w")
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


file.close()




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
