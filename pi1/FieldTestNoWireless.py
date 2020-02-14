from MotorControlFunctions import tankDrive
import inputs
import time


leftY = 0.0
rightY = 0.0

while(True):
    try:
        events = inputs.get_gamepad()
        #sendString = "connected:1:b,"
        for event in events:
            if(event.ev_type == "Absolute"):
                if(event.code == "ABS_Y"):
                    leftY = -(float(event.state)/32768)
                if(event.code == "ABS_RY"):
                    rightY = -(float(event.state)/32768)
            #elif(event.ev_type == "Key"):
            #    sendString += event.code + ":" + str(event.state) + ":b,"
        if(abs(leftY) < 0.15):
            leftY = 0
        if(abs(rightY) < 0.15):
            rightY = 0
        tankDrive(leftY, rightY)
        #time.sleep(0.01)
    except:
        print("Err")
