import serial
import struct

ser = serial.Serial('/dev/ttyUSB0',9600)

def tankDrive(leftPow,rightPow):
    leftOut = int(((leftPow+1.0) * 255)/2)
    rightOut = int(((rightPow+1.0) * 255)/2)
    output = [leftOut, leftOut, rightOut, rightOut]
    ser.write(bytearray(output))
