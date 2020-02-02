import serial
import pynmea2
import time

import sys
import glob
def scan_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        patterns = ('/dev/tty[A-Za-z]*', '/dev/ttyUSB*')
        ports = [glob.glob(pattern) for pattern in patterns]
        ports = [item for sublist in ports for item in sublist]  # flatten
    elif sys.platform.startswith('darwin'):
        patterns = ('/dev/*serial*', '/dev/ttyUSB*', '/dev/ttyS*')
        ports = [glob.glob(pattern) for pattern in patterns]
        ports = [item for sublist in ports for item in sublist]  # flatten
    else:
        raise EnvironmentError('Unsupported platform')
    return ports

scan_ports()
 
'''#define COM-ports
port2 = "COM3"
ser2 = serial.Serial(port2, 4800, timeout=0)
port = "COM2"
ser = serial.Serial(port, 4800, timeout=0)
 
#read from COM-port, parse NMEA and send to new COM-port
streamreader = pynmea2.NMEAStreamReader()
 
while True:
    data = ser2.read()
    for msg in streamreader.next(data):
        msg = pynmea2.GGA('GP', 'GGA', (msg.lat, '1929.045', 'S', '02410.506', 'E', '1', '04', '2.6', '100.00', 'M', '-33.9', 'M', '', '0000'))
         
        while True:
            ser.write(str(msg))
            time.sleep(1)
 
#close COM-ports
ser.close()
ser2.close()'''