#multitouch try
def swipe(xStart,yStart,xEnd,yEnd):
	threading.Thread(target=swipeAux, args=[xEnd,yEnd]).start()
	cmd = 'input touchscreen swipe '+ str(round(xStart*0.01*xRes))+ ' '+ str(round(yStart*0.01*yRes))+' '+ str(round(xStart*0.01*xRes))+ ' '+ str(round(yStart*0.01*yRes))+' 500'
	device.shell(cmd)
	return

def swipeAux(xEnd,yEnd):
	time.sleep(0.2)
	cmd = 'input touchscreen swipe ' + str(round(xEnd)+150)+' '+ str(round(yEnd)+43)+ ' '+str(round(xEnd)+150)+' '+ str(round(yEnd)+43)+ ' 500'
	device.shell(cmd)
	return

def startPuzzle():

	img = cv2.imread('completedPuzzle.png', 0)
	img2 = cv2.imread('completedPuzzle.png', 1)
	#position of the area of puzzle piece we want to search
	xEnd = .8755
	xBeggining = .8469
	yEnd = .16
	yBeggining = .114

	for i in range(35):
		start = time.time()
		image = device.screencap() #take screenshot
		#35 puzzle pieces, search for each piece in the puzzleCompleted.png
		with open(resource_path('puzzleGame.png'), 'wb') as f:
			f.write(image)

		image = Image.open(resource_path('screengt2.png'))
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
		ran= "piece"+str(i)+ ".png"
		#print(ran)
		im.save(resource_path(ran))

		#35 puzzle pieces, search for each piece in the puzzleCompleted.png
		template = cv2.imread('piece'+str(i)+'.png', 0)
		template = cv2.resize(template,(0,0),fx=1.49,fy=1.49, interpolation=cv2.INTER_LINEAR)
		cv2.imwrite(resource_path(ran),template)
		w, h = template.shape[::-1]	#width and height of the template

		res = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED) #result of the match between the template and the completedPuzzle using TM_CCORR_NORMED method
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

		top_left = max_loc[0], max_loc[1] #coordinates of the top left corner of the match of the template within the captchaClean
		bottom_right = (top_left[0] + (w), top_left[1]+ (h))
		cv2.rectangle(img, top_left, bottom_right, (0, 255, 255), -1) #draw a rectangle on what seems the best match
		px=round((top_left[0]+bottom_right[0])/2)
		py=round((top_left[1]+bottom_right[1])/2)

		# Show the final image with the matched area.
		cv2.imshow('Detected',img)
		cv2.imshow('template',template)
		cv2.waitKey(100)
		#here i attempt to use multitouch in adb (that way i could, theoretically, call an input swipe and a tap at the same time to place the piece in the right position, that way i didn't have to place the piece with the swipe, which has a sort of "ruberband" animation, which produces innacurate placements of the pieces, once it travels to fast)
		threading.Thread(target=swipe, args=[86,14,px,py]).start()
		time.sleep(0.7)
		end = time.time()

		print("It took me: ", str(end - start), "s to find 1 object")
