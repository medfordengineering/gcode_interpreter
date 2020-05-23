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

def plotLine(x0, y0, x1, y1):
	points = []
	dx =  abs(x1-x0)
	if  x0 < x1:
		sx =  1 
	else:
		sx = -1

	dy = -abs(y1-y0)
	if y0 < y1:
		sy = 1
	else:
		sy = -1

	err = dx + dy

	while True:
		#print('{}, {}'.format(x0,y0))
		points.append((x0, y0))
		if x0 == x1 and y0 == y1:
			return points
			break
		e2 = 2*err
		if e2 >= dy:
			err += dy 
			x0 += sx

		if e2 <= dx: 
			err += dx
			y0 += sy

def arc(x1, y1, x2, y2, r, d):
	x = x1
	y = y1
	points = []
	while not complete(x,y,x2,y2):
		x, y = nextStep(x,y,r,d)
		points.append((x,y))
		#print('{}, {}xy'.format(x, y))
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

def draw_lines(x_val, y_val):
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
		x_val_total = []
		y_val_total = []
		xi = 0
		yi = 0
		for line in fp:
			mylist = line.split()
			if not len(mylist) == 0:
				if mylist[0] == 'G1' and 'F' not in mylist[1]:
					xf = int(round(float(mylist[1].strip('X'))))
					yf = int(round(float(mylist[2].strip('Y'))))
					points = plotLine(xi, yi, xf, yf) 	

					x_val = [x[0] for x in points] 
					y_val = [x[1] for x in points]
					x_val_total.extend(x_val)
					y_val_total.extend(y_val)

					xi = xf
					yi = yf

				elif mylist[0] == 'G2' or mylist[0] == 'G3':
					xf = int(round(float(mylist[1].strip('X'))))
					yf = int(round(float(mylist[2].strip('Y'))))
					I = int(round(float(mylist[3].strip('I'))))
					J = int(round(float(mylist[4].strip('J'))))

					r = int(round(math.sqrt(I**2 + J**2)))
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

					x_val = [x[0]+xd for x in points] 
					y_val = [x[1]+yd for x in points]
					x_val_total.extend(x_val)
					y_val_total.extend(y_val)

					xi = xf + xd
					yi = yf + yd
		
		draw_lines(x_val_total, y_val_total)
	
def main():
	parse_line()

if __name__ == "__main__":
	main()




