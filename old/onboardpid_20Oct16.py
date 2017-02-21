import sys
import time
from pixy import *
from ctypes import *
from subprocess import Popen, PIPE

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

p = Popen(['./a'], shell=True, stdout=PIPE, stdin=PIPE)
time.sleep(5)

result = 0
integratex = 0
integratey= 0

while 1:
	try:
		count = pixy_get_blocks(100, blocks)
	
		if count > 0:
			vz = -0.15
		
			errx = blocks[0].y - 120
			erry = 160 - blocks[0].x
		
			vx = 0.01 * errx #+ (integratex + errx * 0.00005)  
			vy = 0.01 * erry #+ (integratey + erry * 0.00005)
		
			#integratex = integratex + errx * 0.00005
			#integratey = integratey + erry * 0.00005
		
			if (blocks[0].width * blocks[0].height) > 700:
				land = 1
			else:
				land = 0
		
			#if vx > 2:
			#	vx = 2
			#elif vx < -2:
			#	vx = -2
			#if vy > 2:
			#	vy = 2
			#elif vy < -2:
			#	vy = -2		
		
			value = str(vx) + ' ' + str(vy) + ' ' + str(vz) + ' ' + str(land) + ' ' + str(0) + '\n'	
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
