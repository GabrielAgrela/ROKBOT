#!/usr/bin/env python3

from ppadb.client import Client
from PIL import Image
import numpy
import time
import time
import threading
import webcolors
import yagmail

inReset = False
inAttack = False
updateRunning = False

xRes = 1920
yRes = 1080

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]


def sendEmail(msg):
	print ("sending email with ", msg, " as body.")
	yag = yagmail.SMTP("ithrowthisaway1233321", '123456123456Aa')
	yag.send("gabrielagrela99@gmail.com", "RISE OF KINGDOMS", msg)
#troops died, need healing
def reset():
	global inReset
	print("healing")
	inReset = True
	device.shell(f'input touchscreen swipe 50 950 50 950 200')  #tap city
	time.sleep(0.5)
	device.shell(f'input touchscreen swipe 1747 620 1747 620 100 ')  #tap red cross
	time.sleep(0.5)
	device.shell(f'input touchscreen swipe 1440 864 1440 864 100 ')  #tap heal button
	time.sleep(0.5)
	device.shell(f'input touchscreen swipe 1755 630 1755 630 100 ')  #tap ask help healing
	time.sleep(180) #wait for commander to return
	device.shell(f'input touchscreen swipe 1747 620 1747 620 100 ') #tap recovered troops
	device.shell(f'input touchscreen swipe 50 950 50 950 200') #tap map

	inReset = False
	attackFirstTime()

#Initiated on launched or after troops died
def attackFirstTime():
	global inAttack
	global updateRunning
	print("attacking for the first time")
	inAttack=True
	#device.shell(f'kill-server')
	#time.sleep(5)
	device.shell(f'input touchscreen swipe 50 820 50 820 200') #tap magnifying glass
	device.shell(f'input touchscreen swipe 400 750 400 750 10 ') #tap search button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 960 540 960 540 100 ') #tap barb
	device.shell(f'input touchscreen swipe 1380 723 1380 723 100 ') #tap attack button
	device.shell(f'input touchscreen swipe 1630 215 1630 215 100 ') #tap new troops button
	device.shell(f'input touchscreen swipe 1651 745 1651 745 100 ') #tap button "4" (troops i want to select)
	time.sleep(0.2)
	device.shell(f'input touchscreen swipe 1440 920 1440 920 100 ') #tap march button
	inAttack=False
	if(updateRunning == False):
		update()

#if there's a victory, find and attack new barb
def attack():
	global inAttack
	print("preparing attack")
	inAttack=True
	device.shell(f'input touchscreen swipe 50 820 50 820 200')#tap magnifying glass
	time.sleep(0.2)
	device.shell(f'input touchscreen swipe 400 750 400 750 10 ')#tap search button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 960 540 960 540 100 ')#tap barb
	time.sleep(0.1)
	device.shell(f'input touchscreen swipe 1380 723 1380 723 100 ')#tap attack button
	device.shell(f'input touchscreen swipe 1830 320 1830 320 100 ') #tap army i want
	device.shell(f'input touchscreen swipe 1530 460 1530 460 100 ') #tap march button
	inAttack=False

#manual start - not being used rn
def start():
	device.shell(f'kill-server')
	device.shell(f'input touchscreen swipe 50 820 50 820 200')
	device.shell(f'input touchscreen swipe 400 750 400 750 10 ')
	time.sleep(1)
	device.shell(f'input touchscreen swipe 960 540 960 540 100 ')
	device.shell(f'input touchscreen swipe 1380 723 1380 723 100 ')
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1830 320 1830 320 100 ')
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1530 460 1530 460 100 ')
	update()

#every 4s take a screenshot and analyse it
def update():
	global inAttack
	global inReset
	global updateRunning
	updateRunning = True
	threading.Timer(4.0, update).start() #new thread every 4s
	image = device.screencap() #take screenshot
	with open('screen.png', 'wb') as f: #take screenshot
		f.write(image)
	image = Image.open('screen.png')
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	print ("color of the victory/defeat notification pixel: ", image[830][1467] , " | color of a pixel of the 0AP pop-up: " , image[round(0.8*yRes)][round(0.8*xRes)] , " | color of the position where the CAPTCHA notification pops-up " , image[round(0.1938*yRes)][round(0.8321*xRes)])
	if (image[round(0.1938*yRes)][round(0.8321*xRes)][0] >= 220 and image[round(0.1938*yRes)][round(0.8321*xRes)][0] <= 255 and image[round(0.1938*yRes)][round(0.8321*xRes)][1] >= 225):
		print("CAPTCHA")
		sendEmail("CAPTCHA verification")
	elif ((image[round(0.8*yRes)][round(0.8*xRes)][0] >= 0 and image[round(0.8*yRes)][round(0.8*xRes)][0] <= 50) and (image[round(0.8*yRes)][round(0.8*xRes)][1] >= 70 and image[round(0.8*yRes)][round(0.8*xRes)][1] <= 95) and (image[round(0.8*yRes)][round(0.8*xRes)][2] >= 100 and image[round(0.8*yRes)][round(0.8*xRes)][2] <= 125)): #if no action points
		print ("no action points")
	elif ((image[830][1467][0] >= 220 and image[830][1467][0] <= 250) and (image[830][1467][1] >= 190 and image[830][1467][1] <= 225) and inReset == False): #if defeat notification
		reset()
	elif ((image[830][1467][1] >= 160 and image[830][1467][1] <= 185) and (image[830][1467][0] >= 35 and image[830][1467][0] <= 80) and inAttack == False): #if victory notification
		attack()

attackFirstTime()

time.sleep(1)
