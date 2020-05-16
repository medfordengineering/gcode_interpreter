import matplotlib.pyplot as plt
import numpy as np

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

def test_line():
	points = plotLine(-2,-5,6,9)
	print(points)
	print(type (points))
	print(type (points[1]))
	print(points[len(points) - 1][1])
	#print('x0 = {}, y0 = {}'.format(points[len(points),0], points[len(points),1])

	x_val = [x[0] for x in points]
	y_val = [x[1] for x in points]
	plt.axis([-300, 300, -300, 300])
	plt.minorticks_on()
	plt.grid(which='major', linestyle='solid', linewidth='0.5', color='red')
	plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
	plt.plot(x_val, y_val)
	plt.show()

def main():
	test_line()

if __name__ == "__main__":
	main()

