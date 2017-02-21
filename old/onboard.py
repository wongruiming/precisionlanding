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

while 1:
	try:
		count = pixy_get_blocks(100, blocks)
		if count > 0:
			vz = -0.1
			if blocks[0].x > 180:
				vy = -0.3
			elif blocks[0].x < 140:
				vy = 0.3
			else:
				vy = 0
			if blocks[0].y > 140:
				vx = 0.3
			elif blocks[0].y < 100:
				vx = -0.3
			else:
				vx = 0
				if vy == 0:
					vz = -0.3
			if (blocks[0].width * blocks[0].height) > 600:
				land = 1
			else:
				land = 0
			value = str(vx) + ' ' + str(vy) + ' ' + str(vz) + ' ' + str(land) + ' ' + str(0) + '\n'
			result = p.stdout.readline().strip()	
			p.stdin.write(value)
		else:
			value = str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + '\n'
			result = p.stdout.readline().strip()
			p.stdin.write(value)
			print value
		print result
	except KeyboardInterrupt:
		value = str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(0) + ' ' + str(1) + '\n'
		p.stdin.write(value)
		p.stdin.flush()
		print ("Exiting")
		sys.exit()
