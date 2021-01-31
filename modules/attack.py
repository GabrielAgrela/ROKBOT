def startFarmBarbs():
	global updating
	updating=True
	update()

# check if troops are healed
def checkHopital():
	image = device.screencap() #take screenshot
	with open(resource_path('screen2.png'), 'wb') as f:
		f.write(image)
	image = Image.open(resource_path('screen2.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	print("waiting for healing: ", image[round(0.25*yRes)][round(0.92*xRes)])
	if (checkPixel(0.25,0.92,8,178,230,image) != True): #if army arrived and troops healed/ready to collect
		tap(0.61,0.90) #collect healed troops
		tap(.9,.05) #tap map
		clarionCallAttack()
	else:
		time.sleep(1)
		checkHopital()

#Currently used whenever an army suffers a defeat while farming, or when clarion Call is active and the battle ends
def reset():
	global inReset
	global inEmail
	print("healing")
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(2500, 200)
	inReset = True

	device.shell(f'input touchscreen swipe 50 950 50 950 200')  #tap city
	time.sleep(2)
	tap(.57,.9)#tap red cross
	time.sleep(2)
	#tap(.57,.9)
	device.shell(f'input touchscreen swipe 1440 864 1440 864 100 ')  #tap heal button
	time.sleep(2)
	device.shell(f'input touchscreen swipe 1755 630 1755 630 100 ')  #tap ask help healing
	checkHopital()
	#device.shell(f'input touchscreen swipe 1747 620 1747 620 100 ') #tap recovered troops
	#device.shell(f'input touchscreen swipe 50 950 50 950 200') #tap map

	#inReset = False
	#clarionCallAttack()
def clarionCallAttackInit():
	clarionCallAttack()
	update()
	return

#Currently only used in Clarion Call
def clarionCallAttack():
	global inAttack
	global updateRunning
	global inEmail
	global clarionCall
	global updating

	print("Started Clarion Call")
	winsound.Beep(500, 200)
	time.sleep(0.1)
	inAttack=True
	clarionCall = True
	updating = True



	tap(.75,.05) #tap magnifying glass
	tap(.9,.2) #tap magnifying glass



	"""for i in range(12):
		cmd = 'input touchscreen swipe '+ str(round(.1*xRes))+ ' '+ str(round(.55*yRes))+' '+ str(round(.1*xRes))+' '+ str(round(.55*yRes))+' 10 '
		#print (cmd)
		device.shell(cmd)"""

	"""for i in range(11):
		tap(.55,.32)"""
	tap(.68,.22) #tap search button
	time.sleep(2)
	tap(.5,.5) #tap barb
	time.sleep(1)
	image = device.screencap() #take screenshot
	with open(resource_path('screen2.png'), 'wb') as f:
		f.write(image)
	image = Image.open(resource_path('screen2.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba

	print(image[round(0.65*yRes)][round(0.65*xRes)])
	if (checkPixel(0.65,0.65,230,60,50,image) == None): # if red button doesnt "attack" appear
		threading.Thread(target=clarionCallAttack, args=[]).start()
		return
	print("hey")
	tap(.70,.75) #tap attack button
	time.sleep(1)
	tap(.20,.80) #tap new troops button
	time.sleep(0.2)
	tap(.9,.75) #tap march button

	inAttack=False
	#reset()
	#update()
	return
	"""if(updateRunning == False):
		update()"""

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

	image = device.screencap() #take screenshot
	with open(resource_path('screen2.png'), 'wb') as f:
		f.write(image)
	image = Image.open(resource_path('screen2.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba

	#print(image[round(0.1343*yRes)][round(0.8692*xRes)], " ", checkPixel(0.1343,0.8692,230,0,0,image))
	if (checkPixel(0.66,0.66,230,60,50,image) == None): # if red attack button doesnt appear
		attack()
	if (checkPixel(0.66,0.66,230,60,50,image) == True):
		device.shell(f'input touchscreen swipe 1380 723 1380 723 100 ')#tap attack button
		time.sleep(1)
		device.shell(f'input touchscreen swipe 1830 320 1830 320 100 ') #tap army i want
		time.sleep(1)
		device.shell(f'input touchscreen swipe 1530 460 1530 460 100 ') #tap march button

		inAttack=False

#not working given that the center is always changing
def goHome():
	tap(.1,.85)
	time.sleep(1)
	tap(0.5,.5)
	time.sleep(1)
	tap(0.3,.95)
	time.sleep(1)
	cmd = 'input tap '+ str(round(.57*xRes))+ ' '+ str(round(0.67*yRes))
	#print (cmd)
	device.shell(cmd)
	time.sleep(30)
