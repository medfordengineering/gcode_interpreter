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
		print('{}, {}xy'.format(x, y))
		print('{}, {}x2y2'.format(x2, y2))
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
		print('octant')
		if abs(x) > abs(y):
			return y == y2 
		else:
			return x == x2

def same_octant(x,y,x2,y2):
    return np.sign(x) == np.sign(x2) and np.sign(y) == np.sign(y2) and np.sign(abs(x) - abs(y)) == np.sign(abs(x2) - abs(y2))

def draw_lines(points):
	x_val = [x[0]+xd for x in points] 
	y_val = [x[1]+yd for x in points]
	plt.axis([-300, 300, -300, 300])
	plt.minorticks_on()
	plt.grid(which='major', linestyle='solid', linewidth='0.5', color='red')
	plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
	plt.plot(x_val, y_val)
	plt.show()


def test_arc():
	xi = 276
	yi = 212
	xf = 35
	yf = 133
	#xf = 250
	#yf = 134
	I = -133
	J = 0
	
	r = int(round(math.sqrt(I**2 + J**2)))
	xd = I + xi
	yd = J + yi
	xi = xi - xd
	yi = yi - yd
	xf = xf - xd	
	yf = yf - yd

	#points = arc(xi,yi,xf,yf,r,'CW')

	points = arc(200,0,0,200,200,'CW')
	#points = arc(-30,90,80,-50,95,'CW')
	#x_val = [x[0]+xd for x in points] 
	#y_val = [x[1]+yd for x in points]

	x_val = [x[0] for x in points] 
	y_val = [x[1] for x in points]
	plt.axis([-300, 300, -300, 300])
	#plt.axis([-15, 15, -15, 15])
	plt.minorticks_on()
	plt.grid(which='major', linestyle='solid', linewidth='0.5', color='red')
	plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
	plt.plot(x_val, y_val)
	plt.show()

def parse_line():
	with open(filepath, 'r') as fp:
		gcode = {}
		points = []
		#points_total = []
		x_val_total = []
		y_val_total = []
		xi = 130
		yi = 290
		for line in fp:
			mylist = line.split()
			if not len(mylist) == 0:
				if mylist[0] == 'G1' and 'F' not in mylist[1]:
					X1 = int(round(float(mylist[1].strip('X'))))
					Y1 = int(round(float(mylist[2].strip('Y'))))
					#points = plotLine(X0, Y0, X1, Y1) 	

					#print(*points, sep = '\n')
					print("point")
					#X0 = points[len(points) - 1][0]
					#Y0 = points[len(points) - 1][1]
					#points_total.extend(points)
					#gcode = json.dumps({'G1':[ float(mylist[1].strip('X')), float(mylist[2].strip('Y'))]})
					#gcode = json.dumps({'G1':[ int(round(float(mylist[1].strip('X')))), int(round(float(mylist[2].strip('Y'))))]})
					#print(gcode)
				elif mylist[0] == 'G2' or mylist[0] == 'G3':
					xf = int(round(float(mylist[1].strip('X'))))
					yf = int(round(float(mylist[2].strip('Y'))))
					I = int(round(float(mylist[3].strip('I'))))
					J = int(round(float(mylist[4].strip('J'))))

					r = int(round(math.sqrt(I**2 + J**2)))
					print('{}radius'.format(r))
					xd = I + xi
					yd = J + yi
					xi = xi - xd
					yi = yi - yd
					xf = xf - xd	
					yf = yf - yd

					if mylist[0] == 'G2':
						points = arc(xi,yi,xf,yf,r,'CW')
					else:	
						points = arc(xi,yi,xf,yf,r,'CC')

					#xi = points[len(points) -1][0] + xd
					#yi = points[len(points) -1][1] + yd
					x_val = [x[0]+xd for x in points] 
					y_val = [x[1]+yd for x in points]

					#xi = x_val[len(x_val) -1] 
					#yi = y_val[len(y_val) -1] 
					xi = xf + xd
					yi = yf + yd
		
					#xi = points[len(points) -1][0] 
					#yi = points[len(points) -1][1]

					x_val_total.extend(x_val)
					y_val_total.extend(y_val)
					#points_total.extend(points)
	#draw_lines(points)
		plt.axis([-300, 300, -300, 300])
		#plt.axis([-15, 15, -15, 15])
		plt.minorticks_on()
		plt.grid(which='major', linestyle='solid', linewidth='0.5', color='red')
		plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
		plt.plot(x_val_total, y_val_total)
		plt.show()


					#gcode = json.dumps({'G2':[ float(mylist[1].strip('X')), float(mylist[2].strip('Y')), radius]})
	
def main():
	#test_arc()
	parse_line()

if __name__ == "__main__":
	main()




