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

#not currently working
def checkIfInGame():
	time.sleep(1)
	if(device.shell("pidof com.lilithgame.roc.gp") == ""):
		device.shell("monkey -p com.lilithgame.roc.gp 1")
		#exec(open("rok.py").read())
		os.system("python rok.py")
		sys.exit("Error message")
	threading.Thread(target=checkIfInGame, args=[]).start()
	return
