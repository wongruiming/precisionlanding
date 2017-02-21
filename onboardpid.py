import sys
import time
import math
from pixy import *
from ctypes import *
from subprocess import Popen, PIPE
#from pynput.keyboard import Key, Listener

# Pixy Python SWIG get blocks example #

print ("Pixy Python SWIG Example -- Get Blocks")

# Initialize Pixy Interpreter thread #
pixy_init()

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks = BlockArray(100)

with open('pid.txt', 'r') as f:
	Kp = float(f.readline())
	Kd = float(f.readline())
	Kv = float(f.readline())

p = Popen(['./a'], shell=True, stdout=PIPE, stdin=PIPE)
time.sleep(5)

result = 0
#integratex = 0
#integratey= 0
err_radius = 0
loop = 0
errxlast = 0
errylast = 0
dampx = 0
dampy = 0


while 1:
	try:		 
		count = pixy_get_blocks(100, blocks)
	
		if count > 0:
						
			errx = 120 - blocks[0].y
			erry = blocks[0].x - 160
			
			err_radius=(errx*errx+erry*erry)/40000
			vz = Kv*-1*math.pow(0.1,err_radius)
			
			if loop == 0:
				dampx = 0
				dampy = 0
			else:
				dampx = (errx - errxlast)
				dampy = (erry - errylast)
			
			loop = 1
			
			vx = Kp * errx + Kd * dampx#+ (integratex + errx * 0.00005)  
			vy = Kp * erry + Kd * dampy#+ (integratey + erry * 0.00005)
			
			errxlast = errx
			errylast = erry
			
			#integratex = integratex + errx * 0.00005
			#integratey = integratey + erry * 0.00005
		
			if (blocks[0].width * blocks[0].height) > 225: 
				if err_radius < 0.07:
					land = 1
				else:
					vz = 0
			else:
				land = 0
		
			if vx > 2:
				vx = 2
			elif vx < -2:
				vx = -2
			if vy > 2:
				vy = 2
			elif vy < -2:
				vy = -2		
		
			#value = str(vx) + ' ' + str(vy) + ' ' + str(vz) + ' ' + str(land) + ' ' + str(0) + '\n'
			value = str(vx) + ' ' + str(vy) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + '\n'	
			p.stdin.write(value)
			p.stdin.flush()
			result = p.stdout.readline().strip()
		else:
			value = str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + '\n'
			p.stdin.write(value)
			p.stdin.flush()
			result = p.stdout.readline().strip()
		print value
		print result
		
	except KeyboardInterrupt:
		value = str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(1) + '\n'
		p.stdin.write(value)
		p.stdin.flush()
		time.sleep(3)
		print ("Exiting")
		sys.exit()