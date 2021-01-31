#sends different parameters depending on the button pressed (even though both lyceum challenges, midterm/finals and preliminary, use the same functions, their texts are in different positions)
def lyceumBot():
	global imageG
	#take screenshot
	image = device.screencap()
	start = time.time()
	with open(resource_path('screen.png'), 'wb') as f:
		f.write(image)

	image = Image.open(resource_path('screen.png'))
	image = numpy.array(image, dtype=numpy.uint8) #get screenshot data in rgba
	imageG = image
	end = time.time()
	print("It took me: ", str(end - start), "s to get the screenshot")
	if (midTerm==False):
		threading.Thread(target=getTextFromImage, args=[.2638,.90,.24,.39,True]).start() #get text from title, store it in the queue (like a return)
		threading.Thread(target=chooseAnswer, args=[getTextFromImageQueue.get()]).start() #chooseAnswer thread with the value "returned" from getTextFromImage as an argument
	elif (midTerm==True):
		threading.Thread(target=getTextFromImage, args=[.25,.89,.31,.41,True]).start()
		threading.Thread(target=chooseAnswer, args=[getTextFromImageQueue.get()]).start()

#receives the coordinates of the beggining and end of X and Y in order to crop the screensho, framing only the text we want to extract
def getTextFromImage(xBeggining, xEnd, yBeggining, yEnd, isTitle):
	global imageG
	image = imageG
	xLocal=-1
	yLocal=-1
	xTotalPixels = round((xEnd - xBeggining) * xRes)
	yTotalPixels = round((yEnd - yBeggining) * yRes)

	newImage = numpy.zeros((yTotalPixels+10, xTotalPixels+10, 4)) #newImage is the same kind of array of the screenshot's data

	start = time.time()
	#copy every pixel's color in the given coordinates and paste them, in the respective order, in the newImage's data array, starting at 0
	for x in range(round(xBeggining*xRes), round(xEnd*xRes)):
		xLocal+=1
		yLocal=0
		for y in range(round(yBeggining*yRes), round(yEnd*yRes)):
			yLocal+=1
			#print(xLocal, ",", yLocal, " = ",image[y][x])
			newImage[yLocal][xLocal] = image[y][x]

	end = time.time()
	print("It took me: ", str(end - start), "s to crop image")
	start = time.time()
	#formating the newImage array to the screenshot's type
	newImage = numpy.array(newImage, dtype=numpy.uint8)
	im = Image.fromarray(newImage)
	randomN = randrange(20)
	ran= "screenshots/reading"+str(randomN)+ ".png"
	#print(ran)
	im.save(resource_path(ran))

	#now that we saved the cropped image with the text on it, we need to apply some filters, making it easier for tess to extract its string
	img = cv2.imread(resource_path(ran),0)
	# since the tittle color is black and the options is white, we need different values to filter it
	if (isTitle == True):
		retval, img = cv2.threshold(img, 140,90, cv2.THRESH_BINARY)
	if (isTitle == False):
		retval, img = cv2.threshold(img, 215,250, cv2.THRESH_BINARY)
		img = cv2.bitwise_not(img) #invert colors, so tess can read it black on white (other way around gives much more innacurate results)
	img = cv2.resize(img,(0,0),fx=3,fy=3, interpolation=cv2.INTER_CUBIC) #scaling up helps with accuracy
	#Blurring edges makes them less sharp, tess likes that
	img = cv2.GaussianBlur(img,(11,11),0)
	img = cv2.medianBlur(img,5)
	end = time.time()
	print("It took me: ", str(end - start), "s to edit the image")

	#cv2.imshow('asd',img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	question = tess.image_to_string(img, lang='eng')
	getTextFromImageQueue.put(question.lower())

#stores all questions data and looks for the right answer
def chooseAnswer(question):
	answers = ['louis xiv', 'robert davidson', 'flame altar', 'golden key', 'last of the romans', 'spain', 'germany', 'artiodactyla', 'charlemagne', 'a gladiator', 'descartes', 'nautilus', 'france', 'stephen hawking', 'professor moriarty', 'greenland', 'the crystal palace', 'taj mhal', '20', 'spain', 'the wars of the roses', 'iodine', 'diet of worms', 'louis xi', 'iran', 'talc', 'lancelot', 'goguryeo', 'fossil fuel', 'nuclear', 'the wars of the roses', 'sarka', 'clothing', 'carthage', 'cleopatra vii', 'school of athens', '5', 'minamoto no yoshitsune', 'castle', '25', 'united kingdom', 'seismographs', 'egypt', 'caesar', 'china', 'raoliang', 'chivalry', 'minamoto no yoritomo', 'black', 'papyrus', 'variations', '42.2 km', 'the cerebellum', '1%', 'upgrading castle', '5', 'socrates.', 'lvl. 3 tome of knowledge', 'cavalry', 'infantry', 'hannibal barca', '', 'leonardo da vinci', '3 – old, middle, new', 'leader of the alliance that conquers the lost temple', 'flat/two-dimensional', 'medici', 'medicis', 'mannerism', 'humanism', 'renaissance', '1,000', 'archer', 'minamoto no yoshitsune', 'giving resources to allies.', 'vasco de gama', 'the more offspring produced the more likely they will survive', 'hector', 'upgrading watch tower', 'realistic', 'wealthy patrons', 'because they are more likely to survive and produce…', 'the senate', 'hydroelectric power', 'fission', 'reindeer', 'the wars of the roses', 'tomyris', 'constance', 'lohar', 'lead', 'tomoe gozen', 'tomoe gozen', 'aphrodite', 'rat / mouse', 'ancient rome', 'natural gas', 'vikings', 'geo', 'petroleum', 'classical culture', 'idk', 'idk', 'johann gutenberg', 'pelagius', 'attacking other players', 'school of athens', 'enemy elimination', 'the last supper, mona lisa', 'war of roses', 'hannibal barca', 'the odyssey and the iliad', 'provide a path for salvation', 'baibars', 'on the open seas', 'æthelflæd', 'sydney opera house', 'agriculture', 'jupiter', 'cao cao', 'uncrowned king', '4', 'bartolomeu dias', 'usa', 'vienna', 'father and son', 'machiavelli', 'italy', 'leonardo da vinci', 'china', 'edward viii', 'euclid', 'charles i', 'rule with absolute force', 'the black plague did not hit italy as a result of the alps', 'provide path of salvation', 'photosphere', 'frederick i', 'oceania', 'archimedes', 'by donating to the alliance', 'agriculture', 'his heel', 'dna', 'colonel', 'sparta', 'king henry viii', 'the house of hanover', 'idk', 'idk', 'water', 'hannibal barca', 'cirque du soleil', 'gaius octavius', 'odin', 'the religions', 'birthplace of the renaissance', 'someone who warships 1 god.', 'gandhi', '1000', 'coal', 'maurya', 'africa', 'biomass', 'palace of versailles', 'napoleon bonaparte', 'yi seong-gye', 'yi seong-gye', 'tokugawa ieyasu', 'eye', 'tokugawa ieyasu', 'escort the ark to a non-enemy building', 'the ottomans', 'constantinople', 'natural resources', 'sydney', 'oil', 'achilles; arrow though his heel', 'doctors', 'julius caesar', 'pharaoh', 'cleopatra', 'eyeballs', 'gladiator', 'carthage', 'the red chameleon', 'maurya dynasty', 'michelangelo', 'pericles', 'glorious revolution', 'cerebellum', 'napoleon bonaparte', 'fusion', 'charge', 'tokugawa ieyasu', 'the incas', 'the incas', 'the sumerians', 'spinning', 'cromwell', 'pierre de coubertin', '1776', 'gaius octavius augustus', 'archer', 'palace of versailles', 'coca cola', 'cleopatra vii', 'survive', 'richard i', 'saladin', 'jason', 'odysseus, the greek', 'opera house', 'both mutations and genetic recombination.', 'asia', 'genghis khan', 'natural selection', 'joan of arc', 'sarka', 'only believe in one god.', 'rosetta stone.', 'petroleum', 'hector', '1192', 'genetic variation needed for a population to evolve', 'healing speed up', 'palestine', '1776', 'most of india', 'guitar', 'the phantom of the opera', 'francia', 'ivan the terrible', 'iron', 'cao cao', 'the code of hammurabi', 'marco polo', 'fuzimiao', 'the trojan war', 'camel', 'boudica', 'earthquake', 'eiichiro oda / one piece', 'aristotle', 'aristotle', 'charles martel', 'themselves', 'sun tzu', 'achille']

	questions = ['which of the following french kings was known as the sun king?', 'which inventor built the world?s first electric locomotive in 1837?', 'which type of holy sites grant troop attack bonuses?', 'which of the following can not be found in alliance shops?', 'what is belisarius? nickname?', 'which european country?s king funded christopher columbus? famous expedition?', 'from the 17th to 19th centuries, the kingdom of prussia was mostly in which modern country', 'which mammalian order does suidae belong to?', 'who was believed to be the prototype of king of hearts in poker?', 'what did spartacus do as a slave before leading the biggest slave rebellion of ancient rome?', 'who proposed the philosophical idea of ?i think, therefore i am??', 'which of the following marine species has existed the longest?', 'which country gave the statue of liberty ti american people as a gift?', 'which of the following physicists was born on the death anniversary of galileo galilei, and died on the birth anniversary of albert einstein?', 'who was called ?napoleon of crime? in some of the sherlock holmes stories?', 'which of the following the world?s largest island?', 'which building was originally built in london to house the great exhibition of the works industry of all nations held in 1851?', 'which of the following was built at the order of shah jahan in the memory of his wife mumtaz mahal?', 'how many times is the character 1 used when you write from numbers 1 to number 99?', 'in which country did the carlist wars take place during the 19th century?', 'which war was fought between the bristish houses of lancaster and york for the throne of england?', 'insufficient intake of which element may case thyromegaly?', 'official measure martin luther', 'which french monarch was known as saint louis?', 'which country in asia overlaps with the former parthian empire?', 'what is the softest material known to mankind?', 'one of the knights of the round table', 'the three kingdoms of korea where baekje, silla, and...?', 'which of the following is a nonrenewable energy source (such as coal, oil, or natural gas)?', 'which of the following is an alternative energy source based on splitting heavy atoms into lighter ones to release energy?', 'which war ended the rule of the house of plantagenet and began the rule of the tudors in england?', 'which commander is named death hydromel?', 'which of these is not a natural resource?', 'the punic wars were fought by ancient rome and what other ancient empire?', 'who was the last female pharaoh of the ptolemy dynasty?', 'raphael is best known for his creation of which of the following?', 'how many phases are there in the mightiest governor event?', 'which commander is known as kamakura?s warlord?', 'which of these is used to rally alliance troops?', 'what is the highest level a city hall can reach in rise of kingdoms?', 'which country started the tradition of the 8-hour workday?', 'which of the following was not invented in china?', 'which country is not in europe?', 'which of the following commanders excels at attacking enemy cities?', 'while gutenberg introduced the printing press in europe, his invention was influenced by which country, the first to develop a moveable type?', 'the four major varieties of guzheng in ancient china were the haozhong, luqi, jiaowei, and the??', 'not one of el cid?s skills?', 'with whom did minamoto no yoshitsune raise an army to fight taira no kiyomori?', 'what color is a polar bears skin?', 'egyptians made paper from which material?', 'the differences among a species, like different bird beaks, are called', 'what is the length of a marathon in kilometers?', 'which part of the brain will alcohol affect?', 'what is the troop health bonus you can get from a fully upgraded hospital?', 'what are the books of covenant used for?', 'how many elite commanders are there in the game?', 'the three great philosophers of ancient greece were plato, aristotle, and?', 'which of the following can not be found in a silver chest at the tavern?', 'which unit type is strong against archers?', 'which unit type is strong against cavalry?', 'who is the commander considered an enemy of rome since childhood?', 'which of these commanders was able to defeat the great charles in the battle?', 'who painted the last supper?', 'ancient egyptian history spans how many kingdoms?', 'who is the king of the kingdom?', 'which of the following is not a characteristic of renaissance art?', 'which famous and influential family did the famous renaissance art patron duke lorenzo belong to?', 'wealthy family in florence', 'which of the following was not a pillar of the renaissance?', 'which of the following was a renaissance intellectual movement in which thinkers studied classical texts and focused on human potential and achievements?', 'which period of history from 1300-1600 saw renewed interest in classical culture and led to far reaching changes in art learning and world view?', 'without using buffs, how many action points can a governor have?', 'which unit strong against infantry?', 'which of the following commanders excels at leading cavalry?', 'which of the following does not award individual credits?', 'which portuguese explorer sailed from the cape of good hope to india?', 'why do frogs and other organisms produce so many eggs/offspring?', 'patroclus got killed by?', 'what are arrows of resistance used for?', 'renaissance painters in flanders, as in italy, tended to produce what type of artwork?', 'what provided the major economic support for the renaissance?', 'why are advantageous traits more likely to be passed onto offspring?', 'after its foundation in the 6th century bce, which institution of the roman republic served as a consultative parliament?', 'what is the name for electricity produced by water power using large dams in a river?', 'the process of splitting atoms is known as', 'santa claus travels on a sleigh pulled by what animal?', 'which war was fought between british houses of lancaster and york for the throne of england?', 'which of these was the only commander to defeat cyrus the great in battle?', 'which of the following commanders joined a rebellion against her own husband?', 'which commander is nicknamed the roaring barbarian?', 'which of the following resources cannot be found in your jeans?', 'which commander was paired with minamoto?', 'genpei war', 'in greek mythology, to whom did paris the prince of troy give golden apple inscribed with to the most beautiful goddess?', 'of the 12 chinese zodiac animals, which comes first?', 'which civilization was the first to have public toilets?', 'which of the following is a fossil fuel formed from marine organisms that is often found in folded or tilted layers and used for heating and cooking?', 'from the 8th to the 11th century ce, what did europeans frequently call the scandinavian invaders who frequently ravaged their lands?', 'which of the following is an inexhaustible energy resource that relies on hot magma or hot dry rocks below ground?', 'which of the following is considered an energy source?', 'the renaissance was a ?rebirth? of', 'advantages of johannes gutenberg?s printing press include all of the following except', 'increase in church power', 'who invented the printing press?', 'who founded the kingdom of asturias?', 'which of the following do not give commanders exp?', 'raphael is best known for?', 'which of the following is a phase of the mightiest governor?', 'which of these two were created by leonardo da vinci?', 'which war was fought between the british?', 'which commander is nicknamed carthage?s guardian?', 'what two major works are attributed to homer?', 'which of the following is not an objective of greek mythology?', 'which commander is nicknamed the father of conquest?', 'where do most hurricanes start?', 'which commander is known as the lady of the mercians?', 'which landmark in sydney, australia is shaped like sails?', 'egypt?s economy was primarily based on what?', 'which planet in our solar system rotates the fastest?', 'which commander was part of the battle of red cliffs?', 'what is julius caesar?s nickname?', 'how many fingers does the cartoon character mickey mouse have on each hand?', 'which portuguese explorer was the first european to sail to the southern tip of africa?', 'in which country was air conditioning invented?', 'the two capitals of austria ? hungary were budapest and?', 'in greek mythology, what is the relationship between zeus and hermes?', '?the end justifies the means? was a key belief of the author of ?the prince?. what was his name?', 'where did the renaissance begin?', 'who painted the mona lisa?', 'movable type was first used in which country?', 'the ?windsor knot? was made popular by which king of england?', 'which ancient greek scholar laid the foundations for future european mathematics and authored the ?elements? of geometry?', 'who was the only king of england to be executed?', 'what four words saying did oda nobunaga live by?', 'which of the following is not a reason why the renaissance began in italy?', 'which of the following is not an objective of greek mythology?', 'under normal circumstances, which layer of the sun can we see with the naked eye?', 'which commander is known as barbarossa?', 'which of the following does the green olympic ring represent?', 'which ancient greek physicist famously discovered the concept of buoyancy while taking a bath?', 'how do you get alliance technology credits?', 'egypt?s economy was primarily based on?', 'in greek mythology, what was achilles? only weak point?', 'mutations are a change in what?', 'what honorary rank was the founder of kentucky fried chicken?', 'which city-state of ancient greece was known for its brutal military training and bravery?', 'wales officially became part of the kingdom of great britain during the reign of which king?', 'queen victoria of england was part of which royal house?', 'which of the seven wonders of the world were created to cure the new queen of babylon?s homesickness?', 'the hanging gardens', 'which of the following is a nonrenewable energy source?', 'which commander was considered an enemy of rome from an early age?', 'which art group is known as a ?national treasure? of canada?', 'which roman emperor was named augustus after ending a civil war?', 'in norse mythology, who wielded the weapon gungnir?', 'northern humanists like erasmus were most commonly known for what?', 'during the renaissance, why was florence significant?', 'which of the following describes a monotheist?', 'to whom did india give title mahatma?', 'how many action points can a governor have?', 'which of the following is a name for sedimentary rock formed from decayed plant materiel in swampy areas?', 'ashoka the great was the king of which ancient indian kingdom?', 'on which continent is the human race generally thought to have originated?', 'what is the name for renewable energy derived from burning organic materials such as wood and alcohol?', 'where did king louis xiv of france move the royal court to in 1682?', 'who was the emperor of the first french empire?', 'which of the following commanders excels at leading archers?', 'who founded the joseon dynasty?', 'first general of the edo shogunate?', 'what is the center of a hurricane called?', 'which prominent statesman served as the first general of the edo shogunate at the end of japan?s warring states period?', 'in ark of osiris, where are you supposed to take the ark?', 'which group conquered the byzantine empire?', 'where was the rallying point for the first crusade?', 'which of the following is a term for a valuable material of geologic origin that can be extracted from the earth', 'which city hosted the 2000 summer olympics?', 'which of the following is a liquid fossil fuel formed from marine organisms that is burned to obtain energy and used to manufacture plastics?', 'who killed hector and how achilles die?', 'first created in ancient greece, to which profession does hippocratic oath apply?', 'who instituted the julian calendar?', 'who owned everything in ancient egyptian kingdoms?', 'who was the last female pharaoh of the ptomely dynasty?', 'which part of the human body contains mostly water?', 'before leading the biggest slave rebellion of ancient rome, what was spartacus?', 'the punic wars were fought by ancient rome and what other ancient empire?', 'what is the champion keira?s nickname?', 'ashoka the great was the king of which ancient kingdom?', 'which artist designed st. peter?s basilica in the vatican?', 'who was praised by his countryman as ancient greece?s best and most honest democratic representatives?', 'what is the name of the revolution in 1688 which established the british constitutional monarchy?', 'which part of the brain will alcohol affect?', 'who was the emperor of the first french empire?', 'the process of combining atoms is known as what?', 'which of the following is not pelagius passive skill?', 'which prominent statesman served as the first general of the edo shogunate at the end of japan?s warring states period?', 'which was the only ancient civilization to develop in a tropical jungle rather than a river basin?', 'lost city', 'which ethnic group founded the earliest civilization of mesopotamia?', 'the cone-shaped winds of tornadoes are notable for doing what?', 'who commanded the new army founded by parliament during the english civil war?', 'who is considered the ?father of the modern olympic games?', 'when is the declaration of independence?', 'who was the first emperor of rome?', 'unit type strong against infantry?', 'where did king louis xiv of france move to royal court to in 1682?', 'which beverage was invented by american pharmacist john pemberton?', 'which of the following commander excels at gathering resources?', 'the more genetic variation a population has, the more likely it is that some individual will what?', 'which of the following commanders excels at leading infantry?', 'which of the following was an enemy of richard the lionheart?', 'in greek mythlogy, which hero quested for the golden fleece?', 'who won the trojan horse idea?', 'which landmark in sydney, australia is shaped like sails?', 'where do adaptations come from?', 'where did genghis khan start building his mongolian empire?', 'who was the founder of the mongolian empire?', 'what is the name for the phenomenon by which organisms that are better adapted to the environment survive to pass traits to their offspring?', 'which of the following commanders was part of the hundred years war?', 'which commander was nicknamed mead of death?', 'what is a monotheist?', 'what discovery made the deciphering of hieroglyphics possible ?', 'eyeglasses are composed of quartz, sand, and what?', 'when achilles refuses to fight, patroclus puts on achilles armor, fights the trojans, and dies, who is patroclus killed by?', 'in which year did richard and saladin sign a truce?', 'mutations are important because they bring about what?', 'in ark of osiris which speedup can be used?', 'how did saladin change the middle east?', 'when was the declaration of independence written?', 'the mughal empire carried islam to where?', 'which musical instrument has six strings?', 'the four biggest musicals in the world are cats, les miserables, miss saigon, and?', 'france and germany were both once part of what kingdom?', 'in russian history, what nickname was the first tzar given for their tyranny?', 'which of the following is considered a metallic resource?', 'which commander is known as the conqueror of chaos?', 'which of the babylonian codes of law was the first full set of written laws in recorded history?', 'which european wrote the first travelogue detailing china?s history, culture, and art?', 'china?s crosstalk sketch comedy format originates in three places: tianqiao in beijing, the quanty bazaar in tianjin and where in nanjing?', 'homer?s ?the iliad? focuses on events happening during which war or battle?', 'which of the following is not part of mexico?s flag.?', 'which commander was known as the celtic rose?', 'which type of natural disaster is measured using the richter scale?', 'which is recognized by the guinness book of world records as having the largest cumulative circulation of any single-author comic?', 'in ancient greece, which philosopher liked to discuss ideas on a street which then got the nickname peripatetic school?', 'galileo?s leaning tower of pisa experiment overturned a theory of which ancient greek scientists?', 'which commander showed their military genius in the battle of poitiers in the 8th century ad?', 'where did the soldiers of ancient rome get their weapons and armor?', 'who wrote the art of war?', 'during the trojan war, which greek warrior killed hector?']

	#safety mesure for title reading, not needed given the recent accurate results
	"""try:
		question_list = question.split()
		testingQuestion_list=question_list[-4]
	except:
		print(bcolors.FAIL  + "\nQuestion too short, trying another method... \n"+ bcolors.ENDC)
		if (midTerm== False):
			question = getTextFromImage(.2638, .85, .24, .30,True)
		if (midTerm==True):
			question = getTextFromImage(.2638, .7, .37, .40,True)

		question_list = question.split()"""
	start = time.time()
	global getTextFromImageQueue

	#Midterm/finals have different options positions from preliminary
	if (midTerm==False):
		threading.Thread(target=getTextFromImage, args=[.25, .54, .4, .49,False]).start()
		A = getTextFromImageQueue.get().lower()
		threading.Thread(target=getTextFromImage, args=[.60, .89, .4, .49,False]).start()
		B = getTextFromImageQueue.get().lower()
		threading.Thread(target=getTextFromImage, args=[.25, .54, .54, .62,False]).start()
		C = getTextFromImageQueue.get().lower()
		threading.Thread(target=getTextFromImage, args=[.60, .89, .54, .62,False]).start()
		D = getTextFromImageQueue.get().lower()
	if (midTerm==True):
		threading.Thread(target=getTextFromImage, args=[.25, .52, .48, .55,False]).start()
		A = getTextFromImageQueue.get().lower()
		threading.Thread(target=getTextFromImage, args=[.59, .86, .48, .55,False]).start()
		B = getTextFromImageQueue.get().lower()
		threading.Thread(target=getTextFromImage, args=[.25, .52, .61, .68,False]).start()
		C = getTextFromImageQueue.get().lower()
		threading.Thread(target=getTextFromImage, args=[.59, .86, .61, .68,False]).start()
		D = getTextFromImageQueue.get().lower()
	end = time.time()
	print("It took me: ", str(end - start), "s to get every option")
	print("\n ----------------------------------------------------------------------\n")
	print("\n Q:",question,"\n")
	print("\n A: ", A)
	print("\n B: ", B)
	print("\n C: ", C)
	print("\n D: ", D)

	found = False
	imCertain = True
	certaintyList= []
	start = time.time()
	#compare every question stored in questions with the question read, store their values (0.0 to 1.0) in certaintyList[]
	for i in range(249):
		certaintyList.append(similar(question,questions[i]))

	bestQuestion = certaintyList[0]
	idBestQuestion = 0

	#search for the highest value (and its id), and therefore, the most similar sentence rokbot has to the question in the display (im sure python has a built in function for this...)
	for i in range (249):
		if (bestQuestion<certaintyList[i]):
			bestQuestion = certaintyList[i]
			idBestQuestion=i
	print(bcolors.OKBLUE + "\n Question Found with" ,certaintyList[idBestQuestion] ,"accuracy: \n",questions[idBestQuestion],"\n" + bcolors.ENDC)
	end = time.time()
	print("It took me: ", str(end - start), "s to find the best question")
	threading.Thread(target=searchOption, args=[question,questions[idBestQuestion],answers[idBestQuestion],A,B,D,C]).start() #once found the best question, choose its best option

#receives an answer from chooseAnswer() and checks which option is the most similar
def searchOption(question,bestQuestion, answer,A,B,D,C):
	global questionEnded
	print(bcolors.WARNING  +"\nTrying: ",answer, "\n" + bcolors.ENDC)
	start = time.time()
	answers = similar(answer,A),similar(answer,B),similar(answer,C),similar(answer,D) #stores the rate of similarity (0.0 to 1.0) of each option vs answer on this array

	#searches for the biggest value (most similar option to its answer) and its id
	bestOption = answers[0]
	idBestOption = 0
	for i in range (4):
		print (i, " - ", answers[i])
		if (bestOption<answers[i]):
			bestOption = answers[i]
			idBestOption=i
	end = time.time()
	print("It took me: ", str(end - start), "s to find the best option")
	#if the best option isn't similar enough to the answer, then something went wrong, but the user can still click manually
	if (bestOption < .6):
		webbrowser.open('https://www.google.com/search?q='+question, new=2)
		print(bcolors.FAIL +"Im not sure which option is it, but the answer is either ",answer, " or check the google page I opened"+ bcolors.ENDC)
		questionEnded = True
	#if the best option is similar enough, tap it prgrammatically
	else:
		if (idBestOption == 0):
			print(bcolors.OKGREEN +"It's A - : ",A + bcolors.ENDC)
			threading.Thread(target=tap, args=[.48,.3]).start()
			questionEnded = True
		elif (idBestOption == 1):
			print(bcolors.OKGREEN +"It's: B - ",B + bcolors.ENDC)
			threading.Thread(target=tap, args=[.48,.7]).start()
			questionEnded = True
		elif (idBestOption == 2):
			print(bcolors.OKGREEN +"It's: C - ",C + bcolors.ENDC)
			threading.Thread(target=tap, args=[.61,.3]).start()
			questionEnded = True
		elif (idBestOption == 3):
			print(bcolors.OKGREEN +"It's: D - ",D + bcolors.ENDC)
			threading.Thread(target=tap, args=[.61,.7]).start()
			questionEnded = True
		else:
			print(bcolors.FAIL  +"ROKBOT didn't find an option found with this answer, check his tries, theres probably the right answer there, slightly different to the options in the display\n" + bcolors.ENDC)
			questionEnded = True
	print ("\n Thread Count: ", threading.active_count())
	print("\n ----------------------------------------------------------------------\n")

#functin called by lyceum Preliminary button
def lyceumP():
	global midTerm
	global questionEnded
	midTerm=False
	questionEnded = False
	start = time.time()
	threading.Thread(target=lyceumBot, args=[]).start()
	lockQuestion()
	end = time.time()
	print("It took me: ", str(end - start), "s to get that answer")

#functin called by lyceum midterm/finals button
def lyceumM():
	global midTerm
	global questionEnded
	midTerm=True
	questionEnded = False
	start = time.time()
	threading.Thread(target=lyceumBot, args=[]).start()
	lockQuestion()
	end = time.time()
	print("It took me: ", str(end - start), "s to get that answer")

def lockQuestion():
	while (questionEnded == False):
		time.sleep(0.01)
		lockQuestion()

	return
