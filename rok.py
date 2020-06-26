#!/usr/bin/env python3

from ppadb.client import Client
from PIL import Image
import numpy
import time
import time
import threading
import webcolors

inReset = False
inAttack = False
updateRunning = False

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]

#troops died, need healing
def reset():
	global inReset
	print("healing")
	inReset = True
	device.shell(f'input touchscreen swipe 50 950 50 950 200')  #tap city
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1747 620 1747 620 100 ')  #tap red cross
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1440 864 1440 864 100 ')  #tap heal button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1755 630 1755 630 100 ')  #tap ask help healing
	time.sleep(180) #wait for commander to return
	device.shell(f'input touchscreen swipe 1747 620 1747 620 100 ') #tap recovered troops
	time.sleep(1)
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
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1630 215 1630 215 100 ') #tap new troops button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1651 745 1651 745 100 ') #tap button "4" (troops i want to select)
	time.sleep(1)
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
	device.shell(f'input touchscreen swipe 400 750 400 750 10 ')#tap search button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 960 540 960 540 100 ')#tap barb
	device.shell(f'input touchscreen swipe 1380 723 1380 723 100 ')#tap attack button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 1830 320 1830 320 100 ') #tap army i want
	time.sleep(1)
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
	print (image[830][1467])
	if ((image[830][1467][0] >= 220 and image[830][1467][0] <= 250) and (image[830][1467][1] >= 190 and image[830][1467][1] <= 225) and inReset == False): #if defeat notification
		reset()
	if ((image[830][1467][1] >= 168 and image[830][1467][1] <= 175) and (image[830][1467][0] >= 35 and image[830][1467][0] <= 40) and inAttack == False): #if victory notification
		attack()
	
attackFirstTime()

time.sleep(1)