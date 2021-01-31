#text colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#0 to 1 rate of how similar a is to b
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

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


#change your emails here
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

#Dynamic tap
def tap (yPos, xPos):
	global inTap
	inTap = True
	winsound.Beep(2500, 200)
	cmd = 'input touchscreen swipe '+ str(round(xPos*xRes))+ ' '+ str(round(yPos*yRes))+' '+ str(round(xPos*xRes))+' '+ str(round(yPos*yRes))+' 10 '
	#print (cmd)
	device.shell(cmd)
	time.sleep(.1)
	inTap = False

def zoomOut():
	pyautogui.keyDown('down')
	time.sleep(0.5)
	pyautogui.keyUp('down')

#change your emails here
def showDebug():
	#debug data
	print("\n ------------------------------------------------------------------------------------")
	print("\n Iteration number: ", nIterations)
	print ("\n Thread Count: ", threading.active_count())
	print ("\n Helps: ", nHelps)
	print ("\n New text color: ", image[round(0.7681*yRes)][round(0.5*xRes)], " and ", checkPixel(0.7681,0.5,251,146,146,image))
	print ("\n New victory cords: ", image[round(0.7597*yRes)][round(0.7979*xRes)], " and ", image[round(0.77*yRes)][round(0.7631*xRes)], " and ", checkPixel(0.7713,0.8001,251,146,146,image))
	print ("\n New defeat cords: ", image[round(0.7726*yRes)][round(0.7616*xRes)], " and ", image[round(0.7713*yRes)][round(0.8001*xRes)])
	print ("\n New CAPTCHA cords: ", image[round(0.1938*yRes)][round(0.8147*xRes)], " and ", image[round(0.1938*yRes)][round(0.8321*xRes)], " and ", image[round(0.1343*yRes)][round(0.8692*xRes)])
	print ("\n New AP cords: ", image[round(0.5633*yRes)][round(0.2296*xRes)], " and ", image[round(0.1938*yRes)][round(0.8321*xRes)])
	return

def takeScreenshot():
	image = device.screencap() #take screenshot
	with open(resource_path('screen2.png'), 'wb') as f:
		f.write(image)
	image = Image.open(resource_path('screen2.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	return

#graphical interface initializations
def menu():
	window = tk.Tk()
	getImagePlsBtn = tk.Button(text="getImagePls", command=getImagePls)
	getImagePlsBtn.pack()
	makeTroopsBtn = tk.Button(text="makeTroops", command=makeTroops)
	makeTroopsBtn.pack()
	searchMarauderBtn = tk.Button(text="searchMarauder", command=searchMarauder)
	searchMarauderBtn.pack()
	clarionCallBtn = tk.Button(text="Clerion Call", command=clarionCallAttackInit)
	clarionCallBtn.pack()
	startPuzzleBtn = tk.Button(text="Start Puzzle", command=startPuzzle)
	startPuzzleBtn.pack()
	farmBtn = tk.Button(text="Farm RSS", command=farm)
	farmBtn.pack()
	farmBarbsBtn = tk.Button(text="Farm Barbs", command=startFarmBarbs)
	farmBarbsBtn.pack()
	lyceumBtn = tk.Button(text="Lyceum Preliminary", command=lyceumP)
	lyceumBtn.pack()
	lyceumMidtermBtn = tk.Button(text="Lyceum Midterm/finals", command=lyceumM)
	lyceumMidtermBtn.pack()
	startCaptchaBtn = tk.Button(text="Captcha", command=startCaptcha)
	startCaptchaBtn.pack()
	window.mainloop()
	return
