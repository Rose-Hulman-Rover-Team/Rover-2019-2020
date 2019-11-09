print('Starting')

import time
from roboclaw import Roboclaw

#Windows comport name
#rc = Roboclaw("COM9",38400)
#Linux comport name
rc = Roboclaw("/dev/ttyACM0",38400)
print(rc.Open())
address = 0x80

while True:
	print('Running')
	for k in range(128):
		rc.ForwardM1(address,0)
		#rc.BackwardM2(address,32)
		time.sleep(1)
		print(k)


