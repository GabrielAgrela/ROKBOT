#!/usr/bin/env python3
# coding=utf8
from ppadb.client import Client
from PIL import Image
from difflib import SequenceMatcher
from random import randrange
from os import system
from skimage.measure import compare_ssim as ssim
from scipy import ndimage
import numpy,time,threading,queue,yagmail,random,winsound,os,time,cv2,sys,imagehash,pprint,webbrowser,puautogui
import tkinter as tk
import pytesseract as tess
import matplotlib.pyplot as plt
tess.pytesseract.tesseract_cmd = r'E:\ac\tesseract.exe'
sys.path.append('modules')
import captcha,resource,extras,WIP,makeTroops,buffPlease,puzzle,marauder,lyceum,attack,farm

#Create folder if doesnt exist
try:
    os.makedirs('screenshots')
except OSError as e:
    print("")

os.system("")

# beep = help pressed
# boop = 1st attack
# boop boop = new Attack
# boop beep = healing
# beep boop beep = sending email

# Global Vars
#threading flags
inReset = False
inAttack = False
inFarm = False
updateRunning = False
inEmail = False
inTap = False
questionEnded = False
lookingForQuestion = False
updating = False
clarionCall = False
midTerm=False
#queue storing values from threads (equivalent to a queue of return var from functions)
getTextFromImageQueue=queue.Queue()
#iterative vars
nHelps = 0
nIterations = 0
#"less elegant" pixel checkpoints
obj1LastXPixel=0
obj2LastXPixel=0
obj1FirstXPixel=0
obj2FirstXPixel=0
#set device/emulator resolution
xRes = 1920
yRes = 1080
#default image holder
imageG = numpy.zeros((1080, 1920, 4))

#connect to device/emulator with adb
adb = Client(host='localhost', port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('no device attached')
    quit()

#Prolly a good idea to have only 1 device while running this
device = devices[0]

#every 1s take a screenshot and analyse it
def update():
	global inAttack
	global inReset
	global updateRunning
	global inEmail
	global inTap
	global nHelps
	global nIterations
	global window
	global updating

	time.sleep(2)
	inEmail = False
	updateRunning = True
	nIterations = nIterations + 1

	if (checkPixel(0.6343,0.9804,230,0,0,image) == True and inTap == False): #if theres a alliance help request
		tap(0.67,0.96)
		nHelps = nHelps + 1
	#print ("\n color of the victory/defeat notification pixel: ", image[830][1467] , " \n color of a pixel of the 0AP pop-up: " , image[round(0.8*yRes)][round(0.8*xRes)] , " \n color of the position where the CAPTCHA notification pops-up " , image[round(0.1938*yRes)][round(0.8321*xRes)] , " \n color of the position where the help notification pops-up " , image[round(0.6343*yRes)][round(0.9804*xRes)] , "\n --------------------------------------------------------------------------")
	if (updating == False and checkPixel(0.1938,0.8147,251,252,251,image) == True and checkPixel(0.1938,0.8321,230,230,235,image) == True and checkPixel(0.1343,0.8692,230,0,0,image) == True and inEmail == False): #if theres a CAPTCHA
		print(" I think there's a CAPTCHA")
		"""tap(.16,.85)
		tap(.50,.65)
		time.sleep(6)
		testCaptcha(False)
		sendEmail("CAPTCHA verification solved")"""
	elif (checkPixel(0.5633,0.2296,255,166,58,image) == True and checkPixel(0.1938,0.8321,0,73,107,image) == True  and inEmail == False ): #if no action points
		print (" I think you have no action points")
		sendEmail("NO ACTION POINTS")
		updating = False
		goHome()
	elif (checkPixel(0.7726,0.7616,254,143,144,image) == True and checkPixel(0.7713,0.8001,251,146,146,image) == True and inReset == False): #if defeat notification
		if (clarionCall == True):
			reset()
		elif (clarionCall == False):
			attack()
	elif (checkPixel(0.7597,0.7979,27,169,49,image) == True and checkPixel(0.77,0.7631,8,162,33,image) == True and inAttack == False): #if victory notification
		if (clarionCall == True):
			reset()
		elif (clarionCall == False):
			attack()
	"""elif (checkPixel(0.6343,0.9804,230,0,0,image) == True and inTap == False): #if theres a alliance help request
		tap(0.67,0.96)
		nHelps = nHelps + 1"""
	if (updating == True):
		threading.Thread(target=update, args=[]).start()
	window.update()
