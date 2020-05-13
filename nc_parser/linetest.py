import matplotlib.pyplot as plt
import numpy as np

def newline(dx, dy):

	error = 0
	d1 = dx
	d2 = dy
	limit = abs(dx)

	sx = 1 
	sy = 1 

	if dx <= 0: 
		sx = -1 
	if dy <= 0: 
		sy = -1 

	if abs(dx) < abs(dy):
		limit = abs(dy)
		d1 = dy
		d2 = dx
	
	for x in range(limit):
		# Always move either X or Y one step on each pass depending on initial values
		if abs(dx) >= abs(dy):
			stepperX(sx)
		else:
			stepperY(sy)

		error = abs(error + abs(d2))
		if (2 * error) >= abs(d1): 
			error = error - abs(d1)

			# Depending on error move the corresponding direction one step on each pass
			if abs(dx) >= abs(dy):
				stepperY(sy)
			else:
				stepperX(sx)

def plotLine(x0, y0, x1, y1):
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
		print('{}, {}'.format(x0,y0))
		if x0 == x1 and y0 == y1:
			break
		e2 = 2*err
		if e2 >= dy:
			err += dy 
			x0 += sx

		if e2 <= dx: 
			err += dx
			y0 += sy

def testLineQ1(x0,y0, x1,y1):
	dx = x1 - x0
	dy = y1 - y0
	D = 2*dy - dx
	y = y0

    #for x from x0 to x1
	for x in range(dx+1):
		print('{}, {}'.format(x,y))
		if D > 0:
			y = y + 1
			D = D - 2*dx
		D = D + 2*dy

def test_line():
	#testLineQ1(0,0,15,15)
	plotLine(-2,-5,6,9)

def main():
	test_line()

if __name__ == "__main__":
	main()




