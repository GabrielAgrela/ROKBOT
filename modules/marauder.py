def searchMarauderAux():
	time.sleep(1)
	image = device.screencap() #take screenshot
	with open(resource_path('screenshotMarauder.png'), 'wb') as f:
		f.write(image)

	img = cv2.imread('screenshotMarauder.png', 0)
	img2 = cv2.imread('screenshotMarauder.png', 1)

	template = cv2.imread('marauderIcon.png', 0)

	w, h = template.shape[::-1]	#width and height of the template

	#img3 = img2.copy()

	res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED) #result of the match between the template and the captchaClean using TM_CCOEFF_NORMED method
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	print("max ",max_val)

	if (max_val < .8):
		cmd = 'input touchscreen swipe  800 700 800 200 500'
		device.shell(cmd)
		searchMarauderAux()
		return

	top_left = max_loc[0], max_loc[1] #coordinates of the top left corner of the match of the template within the captchaClean
	#bottom_right = (top_left[0] + (w*2), top_left[1]+ (h*2))
	bottom_right = (top_left[0] + (w), top_left[1]+ (h))
	cv2.rectangle(img2, top_left, bottom_right, (0, 255, 255), -1) #draw a rectangle on what seems the best match
	px=round((top_left[0]+bottom_right[0])/2)
	#px=px-((1440-px)*0.3)
	#py=round((top_left[1]+bottom_right[1])/2*1.4)
	py=round((top_left[1]+bottom_right[1])/2)
	#print("oiii", str(px))
	# Show the final image with the matched area.
	tap(py/1080,px/1920)
	cv2.imshow('Detected',img2)
	cv2.imshow('template',template)
	cv2.waitKey(100)
	time.sleep(1)
	attackMarauder()
	return

def searchMarauder():
	for i in range (4):
		time.sleep(1)
		zoomOut()
		time.sleep(1)
		searchMarauderAux()
	return

def attackMarauder():
	cmd = 'input touchscreen swipe  800 500 850 500 500'
	device.shell(cmd)
	tap(.5,.5) #tap marauder
	tap(.6,.3) #tap attack Button
	tap(.20,.80) #tap new troops button
	tap(.9,.75) #tap march button
