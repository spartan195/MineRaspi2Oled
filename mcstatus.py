# -*- coding:utf-8 -*-

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import sys
import time
import subprocess
import os
import string

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#GPIO define
RST_PIN  = 25 #Reset
CS_PIN   = 8
DC_PIN   = 24
JS_U_PIN = 6  #Joystick Up
JS_D_PIN = 19 #Joystick Down
JS_L_PIN = 5  #Joystick Left
JS_R_PIN = 26 #Joystick Right
JS_P_PIN = 13 #Joystick Pressed
BTN1_PIN = 21
BTN2_PIN = 20
BTN3_PIN = 16

# Some constants
SCREEN_LINES = 4
SCREEN_SAVER = 999999999.0
CHAR_WIDTH = 19
font = ImageFont.load_default()
width = 128
height = 64
x0 = 0
x1 = 84
y0 = -2
y1 = 12
x2 = x1+7
x3 = x1+14
x4 = x1+9
x5 = x2+9
x6 = x3+9

choices = [
	["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"],
	["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
	["0","1","2","3","4","5","6","7","8","9","!","@","#","$","%","^","&","*","(",")",",",".","?",":",";","'"]
]

# init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(JS_U_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_D_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_L_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_R_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(JS_P_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(BTN3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# Initialize the display...
serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = DC_PIN, gpio_RST = RST_PIN)
device = sh1106(serial, rotate=2) #sh1106
draw = ImageDraw.Draw(Image.new('1', (width, height)))
draw.rectangle((0,0,width,height), outline=0, fill=0)

state = 0 #System state: 0 - scrren is off; equal to channel number (e.g. BTN2_PIN, JS_P_PIN) otherwise
horz = 1 #Selection choice: 0 - Right; 1 - Left
vert = 3 #Selection choice: 1 - Top; 2 - Middle; 3 - Bottom
stamp = time.time() #Current timestamp
start = time.time() #Start screen saver count down
iface = ""
idxWin = 0
idxLen = 0
aplist = []
apIndx = -1
pwdLst = []
pwdLen = 0
chaSel = 1 #possible values: 0, 1, 2

def main_fun():
	global idxLen
	global pwdLen
	global apIndx
	with canvas(device) as draw:
		LINE0 = subprocess.check_output("systemctl status minecraft | awk 'BEGIN{ORS=\"\"} BEGIN{print \"Minecraft is \"} FNR == 3 {print $2}'", shell = True)
		LINE1 = subprocess.check_output("mcstatus localhost status | awk 'FNR == 3 {print $1,$2}'", shell = True )
		LINE2 = subprocess.check_output("top -bn1 | awk 'NR==3{printf \"CPU:%.1f%% idle\", $8}'", shell = True )
		LINE3 = subprocess.check_output("free -m | awk 'NR==2{printf \"Mem: %s/%sMB\", $3,$2,$3*100/$2 }'", shell = True)
		LINE4 = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"Temp:%.1fC\", $1/1000}'", shell = True )
		draw.line((86,24,86,48), fill=1, width=0) #left vertical
		draw.line((86,24,104,14), fill=1, width=0) #top left to center
		draw.line((104,14,123,24), fill=1, width=0) #top left to righ
		draw.line((123,24,123,48), fill=1, width=0) #right to right bottom
		draw.line((123,48,104,60), fill=1, width=0) #right bottom to bottom center
		draw.line((104,60,86,48), fill=1, width=0) #Bottom center to left bottom
		draw.line((86,24,104,35), fill=1, width=0) #top left to middle		
		draw.line((104,35,104,60), fill=1, width=0) #Middle bottom to middle
        
		draw.line((86,28,104,40), fill=1, width=0) #lowered top left to middle
		draw.line((104,40,123,28), fill=1, width=0) #lowered middle to top right
		draw.line((86,32,104,44), fill=1, width=0) #lowered top left to middle
		draw.line((104,44,123,32), fill=1, width=0) #lowered middle to top right
        
		draw.polygon(((86,24),(104,14),(123,23)), fill=255)
		draw.polygon(((86,24),(104,35),(123,23)), fill=255)
		draw.text((x0, y0), LINE0, font=font, fill=255)
		if len(LINE1) > CHAR_WIDTH:
			draw.text((x0, y1),   LINE1[:CHAR_WIDTH], font=font, fill=255)
		else:
			draw.text((x0, y1),   LINE1, font=font, fill=255)

		if len(LINE2) > CHAR_WIDTH:
			draw.text((x0, y1*2), LINE2[:CHAR_WIDTH], font=font, fill=255)
		else:
			draw.text((x0, y1*2), LINE2, font=font, fill=255)

		if len(LINE3) > CHAR_WIDTH:
			draw.text((x0, y1*3), LINE3[:CHAR_WIDTH], font=font, fill=255)
		else:
			draw.text((x0, y1*3), LINE3, font=font, fill=255)

		if len(LINE4) > CHAR_WIDTH:
			draw.text((x0, y1*4), LINE4[:CHAR_WIDTH], font=font, fill=255)
		else:
			draw.text((x0, y1*4), LINE4, font=font, fill=255)

try:
	while True:
		stamp = time.time()
		main_fun()
		time.sleep(5)

except:
	print ("Stopped", sys.exc_info())[0]
	raise
GPIO.cleanup()
