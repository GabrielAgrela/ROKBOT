def getImagePls():
	for i in range (10000):
		xEnd = .13
		xBeggining = .06
		yEnd = .905
		yBeggining = .875
		image = device.screencap() #take screenshot
		with open(resource_path('screenPls.png'), 'wb') as f:
			f.write(image)

		image = Image.open(resource_path('screenPls.png'))
		image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
		xLocal=-1
		yLocal=-1
		xTotalPixels = round((xEnd - xBeggining) * xRes)
		yTotalPixels = round((yEnd - yBeggining) * yRes)

		newImage = numpy.zeros((yTotalPixels, xTotalPixels, 4)) #newImage is the same kind of array of the screenshot's data


		#copy every pixel's color in the given coordinates and paste them, in the respective order, in the newImage's data array, starting at 0
		for x in range(round(xBeggining*xRes), round(xEnd*xRes)-1):
			xLocal+=1
			yLocal=0
			for y in range(round(yBeggining*yRes), round(yEnd*yRes)-1):
				yLocal+=1
				#print(xLocal, ",", yLocal, " = ",image[y][x])
				newImage[yLocal][xLocal] = image[y][x]

		#formating the newImage array to the screenshot's type
		newImage = numpy.array(newImage, dtype=numpy.uint8)
		im = Image.fromarray(newImage)
		ran= "screenPlsClean.png"
		#print(ran)
		im.save(resource_path(ran))
		img = cv2.imread(resource_path(ran),0)
		retval, img = cv2.threshold(img, 215,250, cv2.THRESH_BINARY)
		#img = cv2.bitwise_not(img) #invert colors, so tess can read it black on white (other way around gives much more innacurate results)
		img = cv2.resize(img,(0,0),fx=3,fy=3, interpolation=cv2.INTER_CUBIC) #scaling up helps with accuracy
		#Blurring edges makes them less sharp, tess likes that
		img = cv2.GaussianBlur(img,(11,11),0)
		img = cv2.medianBlur(img,5)
		cv2.imshow('template',img)
		cv2.waitKey(1)
		#cv2.imshow('asd',img)
		#cv2.waitKey(0)
		#cv2.destroyAllWindows()
		content = tess.image_to_string(img, lang='eng')
		#print(content)
		if ("pls"  in content.lower() or "plz"  in content.lower() or "please"  in content.lower()):
			print("oi")
			device.shell(f'input touchscreen swipe 300 600 300 500 500')  #tap city
			tap(.65,.10)
			#do stuff
			time.sleep(10)
			tap(.95,.115)
		else:
			device.shell(f'input touchscreen swipe 300 600 300 570 500')  #tap city
		#time.sleep(2)
		"""if ("pls" or "plz" or "please" in content.lower()):
			tap(.75,.10)
			#do stuff
			time.sleep(10)
			tap(.95,.115)"""
