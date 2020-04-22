#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_MOSI   9
#define OLED_CLK   10
#define OLED_DC    11
#define OLED_CS    12
#define OLED_RESET 13
#define _swap_int16_t(a, b) { int16_t t = a; a = b; b = t; }

#define POS		+1
#define NEG 	-1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, OLED_CS);

int aX;
int aY;

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

void plotDelta(int dx, int dy)
{
	int error = 0;
	int d1=dx;
	int d2=dy;
	int limit = abs(dx);

	int sx = POS;
	int sy = POS;

	if (dx <= 0) sx = NEG;
 	if (dy <= 0) sy = NEG;

  	if (abs(dx) < abs(dy)) {
		limit = abs(dy);
		d1=dy;
		d2=dx;
	}
	
  	for (int x = 0; x < limit; x++) {
    	if (abs(dx) >= abs(dy)) {
			stepperX(sx);
    	}
    	else {
			stepperY(sy);
    	}
    	error = abs(error + abs(d2));
    	if ((2 * error) >= abs(d1)) {
      		error = error - abs(d1);
      		if (abs(dx) >= abs(dy)) {
				stepperY(sy);
      		}
      		else {
				stepperX(sx);
      		}
   		}
	}
}

void plotCord(int x, int y) {
	x = (x - aX);
	y = (y - aY);
	plotDelta(x, y);
}

void setup() {
	display.begin(SSD1306_SWITCHCAPVCC);
  	display.setTextColor(SSD1306_WHITE);
	display.clearDisplay();
  	display.setCursor(0, 0);
	display.display();
	Serial.begin(9600);
	plotCord(10,10);
	plotCord(10,30);
	plotCord(30,30);
	plotCord(30,10);
	plotCord(10,10);
}

void loop() {
}
