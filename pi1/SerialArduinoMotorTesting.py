import serial
import struct

ser = serial.Serial('/dev/ttyUSB0',9600)

while True:
    ser.write(struct.pack('>B', 255))
    ser.write(struct.pack('>B', 254))
    ser.write(struct.pack('>B', 254))
    ser.write(struct.pack('>B', 254))
    ser.write(struct.pack('>B', 254))
