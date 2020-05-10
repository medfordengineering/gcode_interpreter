import matplotlib.pyplot as plt
import numpy as np

aX = 0
aY = 0

void stepperX(int dir){
	aX += dir;
	display.drawPixel(aX, aY,  SSD1306_WHITE);
	display.display();
}

void stepperY(int dir){
	aY += dir;
	display.drawPixel(aX, aY, SSD1306_WHITE);
	display.display();
}

def line(dx, dy):

	error = 0
	d1 = dx
	d2 = dy
	limit = abs(dx)

	sx = POS
	sy = POS

	if (dx <= 0): 
		sx = NEG
 	if (dy <= 0): 
		sy = NEG

  	if abs(dx) < abs(dy):
		limit = abs(dy)
		d1 = dy
		d2 = dx
	
	
	for x in range(limit):

    	if abs(dx) >= abs(dy):
			stepperX(sx)
    	else:
			stepperY(sy)
    	error = abs(error + abs(d2))

    	if (2 * error) >= abs(d1): 
      		error = error - abs(d1)
      		if abs(dx) >= abs(dy):
				stepperY(sy)
      		else:
				stepperX(sx)


def plotCord(x, y): 
	x = (x - aX)
	y = (y - aY)
	plotDelta(x, y)

# note that this is only for counterclockwise
def arc(x1, y1, x2, y2, r, d):
	x = x1
	y = y1
	points = []
	while not complete(x,y,x2,y2):
		x, y = nextStep(x,y,r,d)
		points.append((x,y))
		print('{}, {}'.format(x, y))
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

def main():
	#points = arc(300,0,277,144,300)
	# start point + offset
	xd = 165 - 78
	yd = 81 - 0
	#points = arc(75 - xd,168 -yd,90 -xd,223 -yd,79,'CW')
	points = arc(165-xd, 81-yd, 14-xd, 83-yd, 76,'CW')
	#points = arc(200,0,0,200,200,'CC')
	x_val = [x[0] for x in points]
	y_val = [x[1] for x in points]
	#plt.plot(x_val, y_val, color="red", ls="", marker="o", ms=3)
	#plt.axis('scaled')
	#fig, ax = plt.subplots(figsize = (10,10))
	plt.axis([-300, 300, -300, 300])
	#ax.scatter(x_val,y_val)
	plt.plot(x_val, y_val)
	#print(points)
	plt.grid(axis='both')
	plt.show()

if __name__ == "__main__":
	main()




