#farming rss
def farm():
	global inFarm
	print(" Preparing Farmers")
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(2500, 200)
	inFarm=True
	"""tap(0.75,0.05) #tap magnifying glass
	tap(0.9,0.2) #tap magnifying glass"""
	"""for i in range(12):
		cmd = 'input touchscreen swipe '+ str(round(.1*xRes))+ ' '+ str(round(.55*yRes))+' '+ str(round(.1*xRes))+' '+ str(round(.55*yRes))+' 10 '
		#print (cmd)
		device.shell(cmd)"""
	#tap(0.5,0.5) #tap magnifying glass
	"""farmDyn(0.35)
	farmDyn(0.35)
	farmDyn(0.50)
	farmDyn(0.50)"""
	#farmDyn(0.50)
	#farmDyn(0.80)
	farmDyn(0.65)
	farmDyn(0.65)
	farmDyn(0.65)
	farmDyn(0.65)
	inFarm=False
	threading.Thread(target=checkIfArrived, args=[]).start()

#checking if armies arrrived from farming rss
def checkIfArrived():
	global updating
	time.sleep(5)
	tap(.03,.5)
	start = time.time()
	image = device.screencap() #take screenshot
	with open(resource_path('screen2.png'), 'wb') as f:
		f.write(image)
	image = Image.open(resource_path('screen2.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	end = time.time()
	print("It took me: ", str(end - start), "to proccess the image")
	if (checkPixel(0.25,0.92,8,178,230,image) != True): #if army arrived
		updating = False
		tap(.9,0.05)
		tapFarms()
		tap(.9,0.05)
		time.sleep(1)
		clarionCallAttack()
		time.sleep(10)
		threading.Thread(target=farm, args=[]).start()
	else:
		update()
		threading.Thread(target=checkIfArrived, args=[]).start()

#tap town farms to get their rss
def tapFarms():
	time.sleep(1)
	tap(.54,0.38)
	tap(.63,0.45)
	tap(.35,0.53)
	tap(.54,0.60)
	time.sleep(1)

#farm() aux
def farmDyn(Xpos):
	tap(0.75,0.05) #tap magnifying glass
	#tap(0.90,Xpos) #tap cropland
	tap(0.70,Xpos) #tap search
	time.sleep(1)
	tap(0.50,0.50) #tap deposit
	tap(0.70,0.75) #tap send gatherers
	tap(0.20,0.80) #tap new army
	tap(0.87,0.73) #tap march
