#!/usr/bin/env python3
# coding=utf8
from ppadb.client import Client
from PIL import Image
import numpy
import time
import threading
import yagmail
import random
import winsound
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'E:\ac\tesseract.exe'



# beep = help pressed
# boop = 1st attack
# boop boop = new Attack
# boop beep = healing
# beep boop beep = sending email

inReset = False
inAttack = False
inFarm = False
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

def farmDyn(Xpos):
	tap(0.75,0.05) #tap magnifying glass
	tap(0.90,Xpos) #tap cropland
	tap(0.70,Xpos) #tap search
	time.sleep(1)
	tap(0.50,0.50) #tap deposit
	tap(0.70,0.75) #tap send gatherers
	tap(0.20,0.80) #tap new army
	tap(0.87,0.73) #tap march

def farm():
	global inFarm

	print(" Preparing Farmers")
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(500, 200)
	time.sleep(0.1)
	winsound.Beep(2500, 200)

	inFarm=True
	farmDyn(0.35)
	farmDyn(0.50)
	farmDyn(0.80)
	farmDyn(0.65)
	inFarm=False
	print("sleeping for 30 mnts");
	for x in range(35):
		print(30-x,", minutes left")
		time.sleep(60)
	farm()

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
	sleeptTime = random.randint(0, 90)
	time.sleep(sleeptTime)
	device.shell(f'am force-stop com.lilithgame.roc.gp')  #turn off ROK
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
	#print (cmd)
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

def getTextFromImage(xBeggining, xEnd, yBeggining, yEnd):
	xLocal=-1
	yLocal=-1
	xTotalPixels = round((xEnd - xBeggining) * xRes)
	yTotalPixels = round((yEnd - yBeggining) * yRes)

	image = device.screencap() #take screenshot
	with open('screen.png', 'wb') as f: #take screenshot
		f.write(image)
	image = Image.open('screen.png')
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba

	newImage = numpy.zeros((yTotalPixels+10, xTotalPixels+10, 4))

	for x in range(round(xBeggining*xRes), round(xEnd*xRes)):
		xLocal+=1
		yLocal=0
		for y in range(round(yBeggining*yRes), round(yEnd*yRes)):
			yLocal+=1
			#print(xLocal, ",", yLocal, " = ",image[y][x])
			newImage[yLocal][xLocal] = image[y][x]

	newImage = numpy.array(newImage, dtype=numpy.uint8)
	im = Image.fromarray(newImage)
	im.save("reading.png")

	img = Image.open('reading.png')
	question = tess.image_to_string(img)

	return (question)

def chooseAnswer(question):
	answears = ['Louis XIV', 'Robert Davidson', 'Flame Altar', 'Golden Key', 'Last of the Romans', 'Spain', 'Germany', 'Artiodactyla', 'Charlemagne', 'A gladiator', 'Descartes', 'Nautilus', 'France', 'Stephen Hawking', 'Professor Moriarty', 'Greenland', 'The Crystal Palace', 'Taj Mhal', '20', 'Spain', 'The Wars of the Roses', 'Iodine', 'Diet of Worms', 'Louis XI', 'Iran', 'Talc', 'Lancelot', 'Goguryeo', 'Fossil Fuel', 'Nuclear', 'The Wars of the Roses', 'Sarka', 'Clothing', 'Carthage', 'Cleopatra VII', 'School of Athens', '5', 'Minamoto no Yoshitsune', 'Castle', '25', 'United Kingdom', 'Seismographs', 'Egypt', 'Caesar', 'China', 'Raoliang', 'Chivalry', 'Minamoto no Yoritomo', 'Black', 'Papyrus', 'Variations', '42.2 Km', 'The Cerebellum', '1%', 'Upgrading Castle', '5', 'Socrates.', 'Lvl. 3 Tome of knowledge', 'Cavalry', 'Infantry', 'Hannibal Barca', '', 'Leonardo Da Vinci', '3 – Old, Middle, New', 'Leader of the alliance that conquers the lost temple', 'Flat/Two-dimensional', 'Medici', 'Medicis', 'Mannerism', 'Humanism', 'Renaissance', '1,000', 'Archer', 'Minamoto no Yoshitsune', 'Giving resources to allies.', 'Vasco de Gama', 'the more offspring produced the more likely they will survive', 'Hector', 'Upgrading Watch Tower', 'Realistic', 'Wealthy Patrons', 'because they are more likely to survive and produce…', 'The Senate', 'Hydroelectric power', 'Fission', 'Reindeer', 'The Wars of the Roses', 'Tomyris', 'Constance', 'Lohar', 'Lead', 'Tomoe Gozen', 'Tomoe Gozen', 'Aphrodite', 'Rat / Mouse', 'Ancient Rome', 'Natural Gas', 'Vikings', 'Geo', 'Petroleum', 'Classical Culture', 'IDK', 'IDK', 'Johann Gutenberg', 'Pelagius', 'Attacking other players', 'School of Athens', 'Enemy Elimination', 'The Last Supper, Mona Lisa', 'War of Roses', 'Hannibal Barca', 'The Odyssey and the Iliad', 'Provide a path for salvation', 'Baibars', 'On the Open Seas', 'Æthelflæd', 'Sydney Opera House', 'Agriculture', 'Jupiter', 'Cao Cao', 'Uncrowned king', '4', 'Bartolomeu Dias', 'USA', 'Vienna', 'Father and son', 'Machiavelli', 'Italy', 'Leonardo da Vinci', 'China', 'Edward VIII', 'Euclid', 'Charles I', 'Rule With Absolute Force', 'The black plague did not hit Italy as a result of the alps', 'Provide path of salvation', 'Photosphere', 'Frederick I', 'Oceania', 'Archimedes', 'By donating to the Alliance', 'Agriculture', 'His heel', 'DNA', 'Colonel', 'Sparta', 'King Henry VIII', 'The house of Hanover', 'IDK', 'IDK', 'Water', 'Hannibal Barca', 'Cirque du Soleil', 'Gaius Octavius', 'Odin', 'The Religions', 'Birthplace of the Renaissance', 'Someone who warships 1 god.', 'Gandhi', '1000', 'Coal', 'Maurya', 'Africa', 'Biomass', 'Palace of Versailles', 'Napoleon Bonaparte', 'Yi Seong-Gye', 'Yi Seong-Gye', 'Tokugawa Ieyasu', 'Eye', 'Tokugawa Ieyasu', 'Escort the Ark to a non-enemy building', 'The Ottomans', 'Constantinople', 'Natural Resources', 'Sydney', 'Oil', 'Achilles; Arrow though his heel', 'Doctors', 'Julius Caesar', 'Pharaoh', 'Cleopatra', 'Eyeballs', 'Gladiator', 'Carthage', 'The Red Chameleon', 'Maurya Dynasty', 'Michelangelo', 'Pericles', 'Glorious Revolution', 'Cerebellum', 'Napoleon Bonaparte', 'Fusion', 'Charge', 'Tokugawa Ieyasu', 'The Incas', 'The Incas', 'The Sumerians', 'Spinning', 'Cromwell', 'Pierre de Coubertin', '1776', 'Gaius Octavius Augustus', 'Archer', 'Palace of Versailles', 'Coca Cola', 'Cleopatra VII', 'Survive', 'Richard I', 'Saladin', 'Jason', 'Odysseus, The Greek', 'Opera House', 'Both mutations and Genetic recombination.', 'Asia', 'Genghis Khan', 'Natural Selection', 'Joan of Arc', 'Sarka', 'Only believe in one god.', 'Rosetta stone.', 'Petroleum', 'Hector', '1192', 'Genetic Variation needed for a population to evolve', 'Healing Speed Up', 'Palestine', '1776', 'Most of India', 'Guitar', 'The Phantom of the Opera', 'Francia', 'Ivan the Terrible', 'Iron', 'Cao Cao', 'The Code of Hammurabi', 'Marco Polo', 'Fuzimiao', 'The Trojan War', 'Camel', 'Boudica', 'Earthquake', 'Eiichiro Oda / One Piece', 'Aristotle', 'Aristotle', 'Charles Martel', 'Themselves', 'Sun Tzu', 'Achille',]

	questions = ['Which of the following French Kings was known as the Sun King?', 'Which inventor built the world?s first electric locomotive in 1837?', 'Which type of holy sites grant troop attack bonuses?', 'Which of the following can NOT be found in Alliance Shops?', 'What is Belisarius? nickname?', 'Which European country?s king funded Christopher Columbus? famous expedition?', 'From the 17th to 19th centuries, the Kingdom of Prussia was mostly in which modern country', 'Which mammalian order does Suidae belong to?', 'Who was believed to be the prototype of king of hearts in poker?', 'What did Spartacus do as a slave before leading the biggest slave rebellion of Ancient Rome?', 'Who proposed the philosophical idea of ?I think, therefore I am??', 'Which of the following marine species has existed the longest?', 'Which country gave the Statue of Liberty ti American people as a gift?', 'Which of the following physicists was born on the death anniversary of Galileo Galilei, and died on the birth anniversary of Albert Einstein?', 'Who was called ?Napoleon of crime? in some of the Sherlock Holmes stories?', 'Which of the following the world?s largest island?', 'Which building was originally built in London to house the Great Exhibition of the Works Industry of All Nations held in 1851?', 'Which of the following was built at the order of Shah Jahan in the memory of his wife Mumtaz Mahal?', 'how many times is the character 1 used when you write from numbers 1 to number 99?', 'In which country did the Carlist Wars take place during the 19th century?', 'Which war was fought between the Bristish houses of Lancaster and York for the throne of England?', 'Insufficient intake of which element may case thyromegaly?', 'Official measure Martin Luther', 'Which French monarch was known as Saint Louis?', 'Which country in Asia overlaps with the former Parthian empire?', 'What is the softest material known to mankind?', 'One of the Knights of the Round Table', 'The three kingdoms of Korea where Baekje, Silla, and...?', 'Which of the following is a nonrenewable energy source (such as coal, oil, or natural gas)?', 'Which of the following is an alternative energy source based on splitting heavy atoms into lighter ones to release energy?', 'Which war ended the rule of the House of Plantagenet and began the rule of the Tudors in England?', 'Which commander is named death hydromel?', 'Which of these is not a natural resource?', 'The Punic Wars were fought by Ancient Rome and what other Ancient Empire?', 'Who was the last female Pharaoh of the Ptolemy Dynasty?', 'Raphael is best known for his creation of which of the following?', 'How many phases are there in The Mightiest Governor event?', 'Which commander is known as Kamakura?s warlord?', 'Which of these is used to rally alliance troops?', 'What is the highest level a City Hall can reach in Rise of Kingdoms?', 'Which country started the tradition of the 8-hour workday?', 'Which of the following was NOT invented in China?', 'Which country is not in Europe?', 'Which of the following commanders excels at attacking enemy cities?', 'While Gutenberg introduced the printing press in Europe, his invention was influenced by which country, the first to develop a moveable type?', 'The four major varieties of Guzheng in Ancient China were the Haozhong, Luqi, Jiaowei, and the??', 'Not one of El Cid?s skills?', 'With whom did Minamoto no Yoshitsune raise an army to fight Taira no Kiyomori?', 'What color is a polar bears skin?', 'Egyptians made paper from which material?', 'The differences among a species, like different bird beaks, are called', 'What is the length of a marathon in kilometers?', 'Which part of the brain will alcohol affect?', 'What is the troop health bonus you can get from a fully upgraded Hospital?', 'What are the Books of Covenant used for?', 'How many Elite Commanders are there in the game?', 'The three great philosophers of ancient Greece were Plato, Aristotle, and?', 'Which of the following can not be found in a Silver Chest at the Tavern?', 'Which unit type is strong against Archers?', 'Which unit type is strong against Cavalry?', 'Who is the commander considered an enemy of Rome since childhood?', 'Which of these commanders was able to defeat the great Charles in the battle?', 'Who painted The Last Supper?', 'Ancient Egyptian history spans how many kingdoms?', 'Who is the King of the Kingdom?', 'Which of the following is not a characteristic of renaissance art?', 'Which famous and influential family did the famous Renaissance art patron Duke Lorenzo belong to?', 'Wealthy family in Florence', 'Which of the following was not a pillar of the Renaissance?', 'Which of the following was a Renaissance intellectual movement in which thinkers studied classical texts and focused on human potential and achievements?', 'Which period of history from 1300-1600 saw renewed interest in classical culture and led to far reaching changes in art learning and world view?', 'Without using buffs, how many action points can a governor have?', 'Which unit strong against infantry?', 'Which of the following commanders excels at leading cavalry?', 'Which of the following does not award Individual Credits?', 'Which Portuguese explorer sailed from the Cape of Good Hope to India?', 'Why do frogs and other organisms produce so many eggs/offspring?', 'Patroclus got killed by?', 'What are Arrows of Resistance used for?', 'Renaissance painters in Flanders, as in Italy, tended to produce what type of artwork?', 'What provided the major economic support for the renaissance?', 'Why are advantageous traits more likely to be passed onto offspring?', 'After its foundation in the 6th century BCE, which institution of the Roman Republic served as a consultative parliament?', 'What is the name for electricity produced by water power using large dams in a river?', 'The process of splitting atoms is known as', 'Santa Claus travels on a sleigh pulled by what animal?', 'Which war was fought between British houses of Lancaster and York for the throne of England?', 'Which of these was the only commander to defeat Cyrus the great in battle?', 'Which of the following commanders joined a rebellion against her own husband?', 'Which commander is nicknamed the Roaring Barbarian?', 'Which of the following resources cannot be found in your jeans?', 'Which commander was paired with Minamoto?', 'Genpei War', 'In Greek mythology, to whom did Paris the prince of troy give golden apple inscribed with to the most beautiful goddess?', 'Of the 12 Chinese zodiac animals, which comes first?', 'Which Civilization was the first to have public toilets?', 'Which of the following is a fossil fuel formed from marine organisms that is often found in folded or tilted layers and used for heating and cooking?', 'From the 8th to the 11th century CE, what did Europeans frequently call the Scandinavian invaders who frequently ravaged their lands?', 'Which of the following is an inexhaustible energy resource that relies on hot magma or hot dry rocks below ground?', 'Which of the following is considered an energy source?', 'The Renaissance was a ?Rebirth? of', 'Advantages of Johannes Gutenberg?s printing press include all of the following except', 'Increase in church power', 'Who invented the printing press?', 'Who founded the Kingdom of Asturias?', 'Which of the following do not give commanders EXP?', 'Raphael is best known for?', 'Which of the following is a Phase of the Mightiest Governor?', 'Which of these two were created by Leonardo da Vinci?', 'Which war was fought between the British?', 'Which commander is nicknamed Carthage?s Guardian?', 'What two major works are attributed to homer?', 'Which of the following is not an objective of Greek mythology?', 'Which commander is nicknamed the Father of Conquest?', 'Where do most hurricanes start?', 'Which commander is known as the Lady of the Mercians?', 'Which landmark in Sydney, Australia is shaped like sails?', 'Egypt?s economy was primarily based on what?', 'Which planet in our solar system rotates the fastest?', 'Which commander was part of the Battle of Red Cliffs?', 'What is Julius Caesar?s nickname?', 'How many fingers does the cartoon character mickey mouse have on each hand?', 'Which Portuguese explorer was the first European to sail to the southern tip of Africa?', 'In which country was air conditioning invented?', 'The two capitals of Austria ? Hungary were Budapest and?', 'In Greek Mythology, what is the relationship between Zeus and Hermes?', '?The end justifies the means? was a key belief of the author of ?The Prince?. What was his name?', 'Where did the renaissance begin?', 'Who painted the Mona Lisa?', 'Movable type was first used in which country?', 'The ?Windsor knot? was made popular by which king of England?', 'Which ancient Greek scholar laid the foundations for future European mathematics and authored the ?Elements? of geometry?', 'Who was the only king of England to be executed?', 'What four words saying did Oda Nobunaga live by?', 'Which of the following is not a reason why the renaissance began in Italy?', 'Which of the following is not an objective of Greek mythology?', 'Under normal circumstances, which layer of the sun can we see with the naked eye?', 'Which commander is known as Barbarossa?', 'Which of the following does the green Olympic Ring represent?', 'Which Ancient Greek physicist famously discovered the concept of buoyancy while taking a bath?', 'How do you get Alliance Technology credits?', 'Egypt?s economy was primarily based on?', 'In Greek mythology, what was Achilles? only weak point?', 'Mutations are a change in what?', 'What honorary rank was the founder of Kentucky Fried Chicken?', 'Which city-state of Ancient Greece was known for its Brutal military training and bravery?', 'Wales officially became part of the Kingdom of Great Britain during the reign of which King?', 'Queen Victoria of England was part of which royal house?', 'Which of the seven wonders of the world were created to cure the new Queen of Babylon?s homesickness?', 'The Hanging Gardens', 'Which of the following is a nonrenewable energy source?', 'Which commander was considered an enemy of Rome from an early age?', 'Which art group is known as a ?National Treasure? of Canada?', 'Which Roman Emperor was named Augustus after ending a civil war?', 'In Norse mythology, who wielded the weapon Gungnir?', 'Northern Humanists Like Erasmus were most Commonly Known for what?', 'During the Renaissance, why was Florence significant?', 'Which of the following describes a monotheist?', 'To whom did India give title mahatma?', 'How many action points can a governor have?', 'Which of the following is a name for sedimentary rock formed from decayed plant materiel in swampy areas?', 'Ashoka the Great was the king of which Ancient Indian kingdom?', 'On which continent is the human race generally thought to have originated?', 'What is the name for renewable energy derived from burning organic materials such as wood and alcohol?', 'Where did King Louis XIV of France move the royal Court to in 1682?', 'Who was the Emperor of the First French Empire?', 'Which of the following commanders excels at leading archers?', 'Who founded the joseon dynasty?', 'First general of the Edo shogunate?', 'What is the center of a hurricane called?', 'Which prominent statesman served as the first general of the Edo shogunate at the end of Japan?s Warring States period?', 'In Ark of Osiris, where are you supposed to take the Ark?', 'Which group conquered the Byzantine Empire?', 'Where was the rallying point for the First Crusade?', 'Which of the following is a term for a valuable material of geologic origin that can be extracted from the earth', 'Which city hosted the 2000 Summer Olympics?', 'Which of the following is a liquid fossil fuel formed from marine organisms that is burned to obtain energy and used to manufacture plastics?', 'Who killed Hector and how Achilles die?', 'First created in Ancient Greece, to which profession does Hippocratic oath apply?', 'Who instituted the Julian Calendar?', 'Who owned everything in ancient Egyptian Kingdoms?', 'Who was the last female Pharaoh of the Ptomely Dynasty?', 'Which part of the human body contains mostly water?', 'Before leading the biggest slave rebellion of Ancient Rome, what was Spartacus?', 'The punic wars were fought by ancient Rome and what other ancient empire?', 'What is the champion Keira?s nickname?', 'Ashoka the great was the king of which ancient kingdom?', 'Which artist designed St. Peter?s Basilica in the Vatican?', 'Who was praised by his countryman as ancient Greece?s best and most honest democratic representatives?', 'What is the name of the revolution in 1688 which established the British constitutional monarchy?', 'Which part of the brain will alcohol affect?', 'Who was the emperor of the first French Empire?', 'The process Of combining atoms is known as what?', 'Which of the following is not Pelagius passive skill?', 'Which Prominent statesman served as the first general of the Edo Shogunate at the end of Japan?s warring states period?', 'Which was the only ancient civilization to develop in a tropical jungle rather than a river basin?', 'Lost City', 'Which ethnic group founded the earliest civilization of Mesopotamia?', 'The cone-shaped winds of tornadoes are notable for doing what?', 'Who commanded the New Army founded by Parliament during the English Civil War?', 'Who is considered the ?Father of the Modern Olympic Games?', 'When is the declaration of independence?', 'Who was the first Emperor of Rome?', 'Unit type strong against Infantry?', 'Where did king Louis XIV of France move to royal court to in 1682?', 'Which beverage was invented by American pharmacist John Pemberton?', 'Which of the following commander excels at gathering resources?', 'The more genetic variation a population has, the more likely it is that some individual will what?', 'Which commander excels at leading infantry?', 'Which of the following was an enemy of Richard the Lionheart?', 'In Greek mythlogy, which hero quested for the golden fleece?', 'Who won the Trojan horse idea?', 'Which landmark in Sydney, Australia is shaped like sails?', 'Where do adaptations come from?', 'Where did Genghis Khan start building his Mongolian Empire?', 'Who was the founder of the Mongolian Empire?', 'what is the name for the phenomenon by which organisms that are better adapted to the environment survive to pass traits to their offspring?', 'Which of the following commanders was part of the hundred years war?', 'Which commander was nicknamed mead of death?', 'What is a monotheist?', 'What discovery made the deciphering of hieroglyphics possible ?', 'Eyeglasses are composed of quartz, sand, and what?', 'When Achilles refuses to fight, Patroclus puts on Achilles armor, fights the trojans, and dies, who is Patroclus killed by?', 'In which year did Richard and Saladin sign a truce?', 'Mutations are important because they bring about what?', 'In Ark of Osiris which speedup can be used?', 'How did Saladin change the Middle East?', 'When was the Declaration of Independence written?', 'The Mughal Empire carried Islam to where?', 'Which musical instrument has six strings?', 'The four biggest musicals in the world are Cats, Les Miserables, Miss Saigon, and?', 'France and Germany were both once part of what Kingdom?', 'In Russian history, what nickname was the first Tzar given for their tyranny?', 'Which of the following is considered a metallic resource?', 'Which commander is known as the Conqueror of Chaos?', 'Which of the Babylonian Codes of Law was the first full set of written laws in recorded history?', 'Which European wrote the first travelogue detailing China?s history, culture, and art?', 'China?s crosstalk sketch comedy format originates in three places: Tianqiao in Beijing, the Quanty Bazaar in Tianjin and where in Nanjing?', 'Homer?s ?The Iliad? focuses on events happening during which war or battle?', 'Which of the following is not part of Mexico?s flag.?', 'Which commander was known as the Celtic Rose?', 'Which type of natural disaster is measured using the Richter scale?', 'Which is recognized by the Guinness Book of World Records as having the largest cumulative circulation of any single-author comic?', 'In Ancient Greece, which philosopher liked to discuss ideas on a street which then got the nickname Peripatetic School?', 'Galileo?s Leaning Tower of Pisa experiment overturned a theory of which Ancient Greek scientists?', 'Which commander showed their military genius in the Battle of Poitiers in the 8th century AD?', 'Where did the soldiers of Ancient Rome get their weapons and armor?', 'Who wrote the Art of War?', 'During the Trojan War, which Greek warrior killed Hector?']
	question_list = question.split()

	print("\n Q:",question, "key: ",question_list[-3] ,"\n")
	print("\n A: ", getTextFromImage(.25, .54, .4, .49))
	print("\n B: ", getTextFromImage(.60, .89, .4, .49))
	print("\n C: ", getTextFromImage(.25, .54, .54, .62))
	print("\n D: ", getTextFromImage(.60, .89, .54, .62))
	for i in range(249):
		if (question_list[-3] in questions[i]):
			#print (answears[i],"\n")
			searchOption(answears[i])

def searchOption(answear):
	if (answear in getTextFromImage(.25, .54, .4, .49)):
		tap(.45,.3)
	if (answear in getTextFromImage(.60, .89, .4, .49)):
		tap(.45,.7)
	if (answear in getTextFromImage(.25, .54, .54, .62)):
		tap(.58,.3)
	if (answear in getTextFromImage(.60, .89, .54, .62)):
		tap(.6,.7)

#every 4s take a screenshot and analyse it
def update():
	global inAttack
	global inReset
	global updateRunning
	global inEmail
	global inTap
	global nHelps
	global nIterations
	time.sleep(2)
	inEmail = False
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
#threading.Thread(target=farm, args=[]).start()
#update()
lyceumInput = "x"
menuInput = input('1) Attack First time\n2) Run General Bot\n3)Run Lyceum Bot ')
if (menuInput == "1"):
	attackFirstTime()
elif (menuInput == "2"):
	threading.Thread(target=farm, args=[]).start()
elif (menuInput == "3"):
	for x in range(100):
		if (lyceumInput != ""):
			chooseAnswer(getTextFromImage(.2638,.90,.24,.39))
			lyceumInput = input('Press anything to scan the next question')

time.sleep(1)
