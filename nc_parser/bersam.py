import sys
import json
import math

import matplotlib.pyplot as plt
import numpy as np

filepath = sys.argv[-1]

aX = 0
aY = 0
test_points = []

def stepperX(direction):
	global aX 
	aX += direction
	test_points.append((aX,aY))
	#display.drawPixel(aX, aY,  SSD1306_WHITE)
	#display.display()


def stepperY(direction):
	global aY 
	aY += direction
	test_points.append((aX,aY))
	#display.drawPixel(aX, aY, SSD1306_WHITE);
	#display.display()

def arc(x1, y1, x2, y2, r, d):
	x = x1
	y = y1
	points = []
	while not complete(x,y,x2,y2):
		x, y = nextStep(x,y,r,d)
		points.append((x,y))
		#print('{}, {}'.format(x, y))
	return points

def nextStep(x,y,r,d):
	incX = 1
	incY = 1 
	# quadrants 1,2 and moving counter clockwise OR quadrants 3,4 and moving clockwise
	if (y > 0 and d == 'CC') or (y < 0 and d == 'CW'):
		incX = -1
	# quadrants 2,3 and moving counter clockwise OR quadrants 1,4 and moving clockwise
	if (x < 0 and d == 'CC') or (x > 0 and d == 'CW'): 
		incY = -1
	if abs(x) > abs(y): # octants 1,4,5,8 -> definitely change y, maybe change x
		if error(x + incX, y + incY, r) < error(x, y + incY, r):
			x += incX
		y += incY
	else: # octants 2,3,6,7
		if error(x + incX, y + incY, r) < error(x + incX, y, r):
			y += incY
		x += incX
	return x,y

def error(x,y,r):
    return abs(np.square(x) + np.square(y) - np.square(r))

def complete(x, y, x2, y2):
    if same_octant(x, y, x2, y2):
        if abs(x) > abs(y):
            return y == y2
        else:
            return x == x2

def same_octant(x,y,x2,y2):
    return np.sign(x) == np.sign(x2) and np.sign(y) == np.sign(y2) and np.sign(abs(x) - abs(y)) == np.sign(abs(x2) - abs(y2))

def test_arc():
	#points = arc(300,0,277,144,300)
	# start point + offset
	#xd = 165 - 78
	#yd = 81 - 0

	xd = 276 + 133
	yd = 212 - 0

	#points = arc(75 - xd,168 -yd,90 -xd,223 -yd,79,'CW')
	#points = arc(165-xd, 81-yd, 14-xd, 83-yd, 76,'CW')
	#points = arc(276, 212, 250, 134, 133,'CW')
	points = arc(200,0,0,200,200,'CC')
	x_val = [x[0]  for x in points] 
	y_val = [x[1]  for x in points]

	plt.axis([-300, 300, -300, 300])
	plt.minorticks_on()
	plt.grid(which='major', linestyle='solid', linewidth='0.5', color='red')
	plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
	plt.plot(x_val, y_val)
	plt.show()

def parse_line():
	with open(filepath, 'r') as fp:
		gcode = {}
		points = []
		points_total = []
		X0 = 276 
		Y0 = 212 
		for line in fp:
			mylist = line.split()
			if not len(mylist) == 0:
				if mylist[0] == 'G1' and 'F' not in mylist[1]:
					X1 = int(round(float(mylist[1].strip('X'))))
					Y1 = int(round(float(mylist[2].strip('Y'))))
					points = plotLine(X0, Y0, X1, Y1) 	

					#print(*points, sep = '\n')
					print("point")
					X0 = points[len(points) - 1][0]
					Y0 = points[len(points) - 1][1]
					points_total.extend(points)
					#gcode = json.dumps({'G1':[ float(mylist[1].strip('X')), float(mylist[2].strip('Y'))]})
					#gcode = json.dumps({'G1':[ int(round(float(mylist[1].strip('X')))), int(round(float(mylist[2].strip('Y'))))]})
					#print(gcode)
				elif mylist[0] == 'G2':
					X1 = int(round(float(mylist[1].strip('X'))))
					Y1 = int(round(float(mylist[2].strip('Y'))))
					Xoff = X0 - int(round(float(mylist[3].strip('I'))))
					Yoff = Y0 - int(round(float(mylist[4].strip('J'))))
	
					points = arc(75 - xd,168 -yd,90 -xd,223 -yd,79,'CW')
	#
					#opp = float (mylist[3].strip('I'))
					#adj = float (mylist[4].strip('J'))
					#radius = math.sqrt(opp**2 + adj**2)
					#gcode = json.dumps({'G2':[ float(mylist[1].strip('X')), float(mylist[2].strip('Y')), radius]})
				elif mylist[0] == 'G3':
					opp = float (mylist[3].strip('I'))
					adj = float (mylist[4].strip('J'))
					radius = math.sqrt(opp**2 + adj**2)
					gcode = json.dumps({'G3':[ float(mylist[1].strip('X')), float(mylist[2].strip('Y')), radius]})
		print(*points_total, sep = '\n')
		graph_line(points_total)

def main():
	test_arc()

if __name__ == "__main__":
	main()




