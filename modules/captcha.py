import resource, numpy
from PIL import Image
from random import randrange

device=""
xRes=""
yRes=""

def startCaptcha():
	start = time.time()
	tap(.16,.85)
	tap(.50,.65)
	time.sleep(2)
	testCaptcha(False,device,xRes,yRes)
	end = time.time()
	print("It took me: ", str(end - start), "s to find 1 object")

def testCaptcha(whiteBG,deviceT,xResT,yResT):
	global lookingForQuestion,device,xRes,yRes
	device=deviceT
	xRes=xResT
	yRes=yResT
	print("screenshoting captcha")
	screenshotOfCaptcha()
	print("Extracting objects from captcha")
	captchaToObjects()
	if (lookingForQuestion == True):
		lookingForQuestion = False
		testCaptcha(False)
		return
	print("Extracting object 1")
	getObj("1")
	print("Extracting object 2")
	getObj("2")
	print("Extracting image from captcha")
	getPuzzleImageFromCaptcha()
	print("Searching object 1 in image from captcha")
	findObj("1",whiteBG)
	print("Searching object 2 in image from captcha")
	findObj("2",whiteBG)
	print("Checking if i was successful")
	tap(.8,.6)
	checkCaptchaSuccess(whiteBG)
	return
	"""tap(.16,.85)
	tap(.50,.65)
	time.sleep(6)
	lookingForQuestion = False
	testCaptcha(False)"""

#screenshots whole screen and cuts the part where theres the captcha and its info to a png
def screenshotOfCaptcha():
	xLocal=0
	yLocal=0
	image = device.screencap() #take screenshot
	with open(resource.resource_path('captchaDirty.png'), 'wb') as f:
		f.write(image)
	image = Image.open(resource.resource_path('captchaDirty.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba

	xTotalPixels = round((0.66 - 0.34) * xRes)
	#print(xTotalPixels)
	yTotalPixels = round((0.87 - 0.125) * yRes)
	#print(round(0.95*xRes)-10)
	newImage = numpy.zeros((yTotalPixels+10, xTotalPixels+10, 4)) #newImage is the same kind of array of the screenshot's data
	for x in range(round(0.34*xRes), round(0.66*xRes)-10):
		xLocal+=1
		yLocal=0
		for y in range(round(0.125*yRes), round(0.87*yRes)-10):
			yLocal+=1
			#print(xLocal, ",", yLocal, " = ",image[y][x])
			newImage[yLocal][xLocal] = image[y][x]
	#saving new image with the dimensions and content of the captcha inside the screenshot
	newImage = numpy.array(newImage, dtype=numpy.uint8)
	im = Image.fromarray(newImage)
	randomN = randrange(20)
	im = im.resize((450, 580), Image.ANTIALIAS)
	ran= "captcha.png"
	#print(ran)
	im.save(resource.resource_path(ran))
	return

#opens the captcha png and its info to extract the objects needed to a png
def captchaToObjects():
	global obj1FirstXPixel
	global obj1LastXPixel
	global obj2FirstXPixel
	global obj2LastXPixel
	global lookingForQuestion
	obj1FirstXPixel=0
	obj1LastXPixel=0
	obj2FirstXPixel=0
	obj2LastXPixel=0
	xLocal=0
	yLocal=0

	image = Image.open(resource.resource_path('captcha.png'))
	image = numpy.array(image, dtype=numpy.uint8)

	#dimensions of the objects location (static at the momment)
	xTotalPixels = round(449 - 210)
	yTotalPixels = round(72-2)

	blackOnce = False

	#print("------------------------------")
	newImage = numpy.zeros((yTotalPixels+2, xTotalPixels+2, 4)) #image of the objects "placeholder"
	#populate newImage with the pixels of the objects from captcha while also checking if theres only 2 objects
	for x in range(210, 410):
		xLocal+=1
		yLocal=0
		onWhite=True
		#print(newImage[35][xLocal-1][0])
		if (xLocal-1>2):
			#print(newImage[30][xLocal-1][0])
			if (newImage[30][xLocal-1][0]>250):
				#print("white",xLocal-1)
				if (obj1FirstXPixel != 0 and obj1LastXPixel == 0):
					#print("ob1 ends")
					obj1LastXPixel=xLocal-1
				if(obj2FirstXPixel != 0 and obj2LastXPixel ==0):
					#print("ob2 ends")
					obj2LastXPixel=xLocal-1
			if (newImage[30][xLocal-1][0]<50):
				#print("black ",xLocal-1)
				if (obj1FirstXPixel == 0):
					#print("ob1 starts")
					obj1FirstXPixel=xLocal-1
				if (blackOnce == True and newImage[35][xLocal-1][0] != 0.0):
					#print("ob3 starts") #ob3 start, therefore theres more than 2 objects, re-roll the captcha to find an easier one
					print("looks like there are too many objects, re-rolling...")
					tap(.16,.85)
					tap(.50,.65)
					time.sleep(6)
					lookingForQuestion = True
					return
				if (obj2LastXPixel != 0):
					blackOnce = True
				if (obj1LastXPixel != 0 and obj2FirstXPixel == 0):
					#print("ob2 comeca")
					obj2FirstXPixel = xLocal-1
		for y in range(2, 72):
			yLocal+=1
			#print(xLocal, ",", yLocal, " = ",image[y][x])
			newImage[yLocal][xLocal] = image[y][x]

	#config image with objects and save it
	newImage = numpy.array(newImage, dtype=numpy.uint8)
	im = Image.fromarray(newImage)
	randomN = randrange(20)
	ran= "ob1and2.png"
	im.save(resource.resource_path(ran))

	#usually each image is cropped too thin, so i give it a little room
	obj1LastXPixel = obj1LastXPixel+15
	obj2LastXPixel = obj2LastXPixel+15
	obj1FirstXPixel = obj1FirstXPixel-15
	obj2FirstXPixel = obj2FirstXPixel-15
	return

#get individual image of one object from the image with the objects
def getObj(objN):

	image = Image.open(resource.resource_path('ob1and2.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get data in rgba

	#obj Y is always the same but X depends on the values found in captchaToObjects()
	if(objN == "1"):
		xTotalPixels = round(obj1LastXPixel - obj1FirstXPixel)
	else:
		xTotalPixels = round(obj2LastXPixel - obj2FirstXPixel)
	yTotalPixels = round(50)
	xLocal=0
	yLocal=0
	newImage = numpy.zeros((yTotalPixels+2, xTotalPixels+2, 4)) #image of the object "placeholder"
	#populate new image with the right dimensions and pixels of each object from the ob1and2.png
	if(objN == "1"):
		for x in range(obj1FirstXPixel, obj1LastXPixel):
			xLocal+=1
			yLocal=0
			for y in range(5, 55):
				yLocal+=1
				#print(xLocal, ",", yLocal, " = ",image[y][x])
				newImage[yLocal][xLocal] = image[y][x]
	else:
		for x in range(obj2FirstXPixel, obj2LastXPixel):
			xLocal+=1
			yLocal=0
			for y in range(5, 55):
				yLocal+=1
				#print(xLocal, ",", yLocal, " = ",image[y][x])
				newImage[yLocal][xLocal] = image[y][x]

	#config new obN.png
	newImage = numpy.array(newImage, dtype=numpy.uint8)
	im = Image.fromarray(newImage)
	randomN = randrange(20)
	ran= "ob"+objN+".png"
	#print(ran)
	im.save(resource.resource_path(ran))
	return

#In order to get the best result possible, isolate the puzzle image from captcha from all its irrelevand info
def getPuzzleImageFromCaptcha():

	image = Image.open(resource.resource_path('captcha.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get data in rgba

	#image dimensions (static atm)
	xTotalPixels = round(440)
	yTotalPixels = round(500-75)

	xLocal=0
	yLocal=0
	newImage = numpy.zeros((yTotalPixels+2, xTotalPixels+2, 4)) #clean captcha image "placeholder"
	for x in range(0, 440):
		xLocal+=1
		yLocal=0
		for y in range(75, 500):
			yLocal+=1
			#print(xLocal, ",", yLocal, " = ",image[y][x])
			newImage[yLocal][xLocal] = image[y][x]

	#config captchaClean.png
	newImage = numpy.array(newImage, dtype=numpy.uint8)
	im = Image.fromarray(newImage)
	randomN = randrange(20)
	ran= "captchaClean.png"
	im.save(resource.resource_path(ran))
	return

#algorithm where the match between the obN.png and the captchaClean.png is found
def findObj(objN,whiteBG):
	maxValue=0
	maxI=0
	maxj=0
	maxX=0
	px=0
	py=0
	#try six different cv2.Threshold values (basically change contrast and light)
	for x in range(6):
		#print("X: "+str(x)+"/6")
		img = cv2.imread("captchaClean.png",0)
		retval, img = cv2.threshold(img, x*40,230, cv2.THRESH_TOZERO)
		cv2.imwrite("screenshots/captcha.png",img)

		method = cv2.TM_SQDIFF_NORMED

		template = cv2.imread("ob"+objN+".png", 0)
		#every other X change from black and white to white and black, higher chance of success this way
		if x % 2 != 0:
			whiteBG = False
			template = cv2.bitwise_not(template)
		else:
			whiteBG = True

		#every 10 iterations make the obN bigger
		for i in range (10):
			if(i != 0):
				template = cv2.imread("template/tmpl"+str(i-1)+"angle0.png", 0)
			template = cv2.resize(template,(0,0),fx=1.1,fy=1.1, interpolation=cv2.INTER_CUBIC)

			#every 36 iterations rotate objN 10º
			for j in range (36):
				img = cv2.imread('screenshots/captcha.png', 0)
				img2 = cv2.imread('screenshots/captcha.png', 1)
				template=rotate_image(template, 10,whiteBG)
				cv2.imwrite("template/tmpl"+str(i)+"angle"+str(j*10)+".png",template)

				w, h = template.shape[::-1]	#width and height of the template

				#img3 = img2.copy()

				res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED) #result of the match between the template and the captchaClean using TM_CCOEFF_NORMED method
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

				top_left = max_loc #coordinates of the top left corner of the match of the template within the captchaClean
				bottom_right = (top_left[0] + w, top_left[1] + h)

				cv2.rectangle(img2, top_left, bottom_right, (0, 255, 0), 2) #draw a rectangle on what seems the best match

				#every time theres a better match than the previously best match, update it and store it's max values
				if (numpy.amax(res) > maxValue):
					maxValue= numpy.amax(res)
					px=top_left[0]*1.3  + w # X position where ROKBOT has to tap (there has a resizing of the captcha, so it has to be resized here by 1.3)
					py=top_left[1]*1.3 + h # Y position where ROKBOT has to tap (there has a resizing of the captcha, so it has to be resized here by 1.3)
					maxI = i
					maxJ = j
					maxX = x
					cv2.imwrite("bestMatch"+objN+".png",img2)

	#once finished, tap the location with the best match
	tap(((py)+(yRes*0.213))/yRes,((px)+(xRes*0.34))/xRes)

	#print(((py)+(yRes*0.213))/yRes, " ",((px)+(xRes*0.34))/xRes)
	#print(str(maxValue)+" "+str(maxI)+" "+str(maxJ)+" "+str(maxX))
	return

#check if the tapped results give a success notification, if not, re-roll to new captcha
def checkCaptchaSuccess(whiteBG):
	image = device.screencap() #take screenshot
	with open(resource.resource_path('resultCaptcha.png'), 'wb') as f:
		f.write(image)
	image = Image.open(resource.resource_path('resultCaptcha.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	if (checkPixel(0.77,0.55,222,113,91,image) == True):
		#if (checkPixel(0.5194,0.6729,222,113,91,image) != True):
		tap(.16,.85)
		tap(.50,.65)
		time.sleep(6)
		testCaptcha(whiteBG)
	return

def rotate_image(image, angle,whiteBG):
	image_center = tuple(numpy.array(image.shape[1::-1]) / 2)
	rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
	if (whiteBG == True):
		result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LANCZOS4, borderValue=(255,255,255))
	else:
		result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT)
	return result
