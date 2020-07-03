#!/usr/bin/env python3

from ppadb.client import Client
from PIL import Image
import numpy
import time
import threading
import yagmail
import random
import winsound

# beep = help pressed
# boop = 1st attack
# boop boop = new Attack
# boop beep = healing
# beep boop beep = sending email

inReset = False
inAttack = False
updateRunning = False
inEmail = False
inTap = False

nHelps = 0
nIterations = 0

xRes = 1920
yRes = 1080

#start adb device
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()

#Prolly a good idea to have only 1 device while running this
device = devices[0]

#setting what the MAX R, G or B should be given a color value
def setMax(color):
	if(color >= 225):
		return (255)
	else:
		return (color + 25)

#setting what the MIN R, G or B should be given a color value
def setMin(color):
	if(color <= 25):
		return (0)
	else:
		return (color - 25)

#check if pixel color is within 25 units (positive or negative) in R G and B vectors
def checkPixel (yPos, xPos, colorR, colorG, colorB, image):
	colorRMax = setMax(colorR)
	colorRMin = setMin(colorR)

	colorGMax = setMax(colorG)
	colorGMin = setMin(colorG)

	colorBMax = setMax(colorB)
	colorBMin = setMin(colorB)

	if ((image[round(yPos*yRes)][round(xPos*xRes)][0] >= colorRMin and image[round(yPos*yRes)][round(xPos*xRes)][0] <= colorRMax) and (image[round(yPos*yRes)][round(xPos*xRes)][1] >= colorGMin and image[round(yPos*yRes)][round(xPos*xRes)][1] <= colorGMax) and (image[round(yPos*yRes)][round(xPos*xRes)][2] >= colorBMin and image[round(yPos*yRes)][round(xPos*xRes)][2] <= colorBMax)):
		return True

def sendEmail(msg):
	global inEmail
	inEmail = True
	print ("sending email with ", msg, " as body.")
	winsound.Beep(2500, 200)
	time.sleep(0.1)
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(2500, 200)
	yag = yagmail.SMTP("ithrowthisaway1233321", '123456123456Aa')
	yag.send("gabrielagrela99@gmail.com", "RISE OF KINGDOMS", msg)
	#sleeptTime = random.randint(0, 90)
	#time.sleep(sleeptTime)
	#device.shell(f'am force-stop com.lilithgame.roc.gp')  #turn off ROK
	return

# check if troops are healed
def checkHopital():
	image = device.screencap() #take screenshot
	with open('screen2.png', 'wb') as f: #take screenshot
		f.write(image)
	image = Image.open('screen2.png')
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	time.sleep(5)
	print("waiting for healing~: ", image[round(0.6163*yRes)][round(0.9302*xRes)])
	if (checkPixel(0.6163,0.9302,230,230,235,image) == True):
		time.sleep(5)
		return checkHopital()
	else:
		return

#troops died, need healing
def reset():
	global inReset
	global inEmail
	print("healing")
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(2500, 200)
	inReset = True
	device.shell(f'input touchscreen swipe 50 950 50 950 200')  #tap city
	time.sleep(0.5)
	device.shell(f'input touchscreen swipe 1747 620 1747 620 100 ')  #tap red cross
	time.sleep(0.5)
	device.shell(f'input touchscreen swipe 1440 864 1440 864 100 ')  #tap heal button
	time.sleep(0.5)
	device.shell(f'input touchscreen swipe 1755 630 1755 630 100 ')  #tap ask help healing
	time.sleep(90)
	#checkHopital()
	device.shell(f'input touchscreen swipe 1747 620 1747 620 100 ') #tap recovered troops
	device.shell(f'input touchscreen swipe 50 950 50 950 200') #tap map

	inReset = False
	attackFirstTime()

#Initiated on launched or after troops died
def attackFirstTime():
	global inAttack
	global updateRunning
	global inEmail
	print(" attacking for the first time")
	winsound.Beep(500, 200)
	time.sleep(0.1)
	inAttack=True
	#device.shell(f'kill-server')
	#time.sleep(5)
	device.shell(f'input touchscreen swipe 50 820 50 820 200') #tap magnifying glass
	device.shell(f'input touchscreen swipe 400 750 400 750 10 ') #tap search button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 960 540 960 540 100 ') #tap barb
	device.shell(f'input touchscreen swipe 1380 723 1380 723 100 ') #tap attack button
	time.sleep(0.2)
	device.shell(f'input touchscreen swipe 1630 215 1630 215 100 ') #tap new troops button
	time.sleep(0.2)
	device.shell(f'input touchscreen swipe 1651 745 1651 745 100 ') #tap button "4" (troops i want to select)
	time.sleep(0.2)
	device.shell(f'input touchscreen swipe 1440 920 1440 920 100 ') #tap march button
	inAttack=False
	if(updateRunning == False):
		update()

#Dynamic tap
def tap (yPos, xPos):
	global inTap
	inTap = True
	winsound.Beep(2500, 200)
	cmd = 'input touchscreen swipe '+ str(round(xPos*xRes))+ ' '+ str(round(yPos*yRes))+' '+ str(round(xPos*xRes))+' '+ str(round(yPos*yRes))+' 100 '
	print (cmd)
	device.shell(cmd)
	time.sleep(1)
	inTap = False

#if there's a victory, find and attack new barb
def attack():
	global inAttack
	global inEmail
	print(" preparing attack")
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(500, 200)
	inAttack=True
	device.shell(f'input touchscreen swipe 50 820 50 820 200')#tap magnifying glass
	time.sleep(1)
	device.shell(f'input touchscreen swipe 400 750 400 750 10 ')#tap search button
	time.sleep(1)
	device.shell(f'input touchscreen swipe 960 540 960 540 100 ')#tap barb
	time.sleep(1)
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
	global inEmail
	global inTap
	global nHelps
	global nIterations
	updateRunning = True
	nIterations = nIterations + 1
	image = device.screencap() #take screenshot
	with open('screen.png', 'wb') as f: #take screenshot
		f.write(image)
	image = Image.open('screen.png')
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	print("\n ------------------------------------------------------------------------------------")
	print("\n Iteration number: ", nIterations)
	print ("\n Thread Count: ", threading.active_count())
	print ("\n Helps: ", nHelps)
	print ("\n New victory cords: ", image[round(0.7597*yRes)][round(0.7979*xRes)], " and ", image[round(0.77*yRes)][round(0.7631*xRes)])
	print ("\n New defeat cords: ", image[round(0.7726*yRes)][round(0.7616*xRes)], " and ", image[round(0.7713*yRes)][round(0.8001*xRes)])
	print ("\n New CAPTCHA cords: ", image[round(0.1938*yRes)][round(0.8147*xRes)], " and ", image[round(0.1938*yRes)][round(0.8321*xRes)], " and ", image[round(0.1343*yRes)][round(0.8692*xRes)])
	print ("\n New AP cords: ", image[round(0.5633*yRes)][round(0.2296*xRes)], " and ", image[round(0.1938*yRes)][round(0.8321*xRes)])
	#print ("\n color of the victory/defeat notification pixel: ", image[830][1467] , " \n color of a pixel of the 0AP pop-up: " , image[round(0.8*yRes)][round(0.8*xRes)] , " \n color of the position where the CAPTCHA notification pops-up " , image[round(0.1938*yRes)][round(0.8321*xRes)] , " \n color of the position where the help notification pops-up " , image[round(0.6343*yRes)][round(0.9804*xRes)] , "\n --------------------------------------------------------------------------")
	if (checkPixel(0.1938,0.8147,251,252,251,image) == True and checkPixel(0.1938,0.8321,230,230,235,image) == True and checkPixel(0.1343,0.8692,230,0,0,image) == True and inEmail == False): #if theres a CAPTCHA
		print(" I think there's a CAPTCHA")
		sendEmail("CAPTCHA verification")
	elif (checkPixel(0.5633,0.2296,255,166,58,image) == True and checkPixel(0.1938,0.8321,0,73,107,image) == True  and inEmail == False ): #if no action points
		print (" I think you have no action points")
		sendEmail("NO ACTION POINTS")
	elif (checkPixel(0.7726,0.7616,254,143,144,image) == True and checkPixel(0.7713,0.8001,251,146,146,image) == True and inReset == False): #if defeat notification
		reset()
	elif (checkPixel(0.7597,0.7979,27,169,49,image) == True and checkPixel(0.77,0.7631,8,162,33,image) == True and inAttack == False): #if victory notification
		attack()
	elif (checkPixel(0.6343,0.9804,230,0,0,image) == True and inTap == False): #if theres a alliance help request
		tap(0.67,0.96)
		nHelps = nHelps + 1
	threading.Thread(target=update, args=[]).start()

#attackFirstTime()
#help(0.67,0.96)
update()

time.sleep(1)
