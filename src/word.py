import os, pygame, random

# TODO: Duplicate code in TextMover
class Word:
	def __init__(self,main):
		self.main = main
		self.drawPriority = 2

		self.wordBank = self.getWordList('wordBank')
		self.happyWordBank = self.getWordList('happyWordBank')
		self.HAPPY_WORD_CHANCE = 0.5 #Chance a word will be chosen from the happy bank.

		self.letterSpacing = self.main.FIELD_WIDTH/13
		self.fontSize = int(self.letterSpacing * 1.5)
		self.boldFontSize = int(self.letterSpacing * 1.6)

		self.font = pygame.font.Font(os.path.join('data', 'font', 'wordFont.ttf'), self.fontSize)
		self.boldFont = pygame.font.Font(os.path.join('data', 'font', 'wordFontB.ttf'), self.boldFontSize)
		self.boldFont.set_bold(True)

		self.textY = self.main.FIELD_HEIGHT/2
		self.textCenterX = self.main.FIELD_WIDTH/2

		self.resetWord()

		#Letters are rendered seperately
		self.notDoneColor = (0,0,0); self.notDoneColorB = (255,255,255)
		self.doneColorB = (255,255,255) #self.doneColor changes over time

		self.doneColorHue = 0; self.doneColorHueChange = 1

		self.MAX_LOSE_RECOIL_TIME = 60
		self.loseRecoilTime = 0

	def compute(self):
		self.doneColorHue += self.doneColorHueChange
		if self.doneColorHue >= 360: self.doneColorHue -= 360

		if self.loseRecoilTime > 0: self.loseRecoilTime -= 1

	def draw(self,surface):
		# Draw pale ellipse so word is easier to see
		frEllipse = 0.75
		w, h = surface.get_width(), surface.get_height()
		s = pygame.Surface((w * frEllipse, h * frEllipse), pygame.SRCALPHA)
		s.fill((0, 0, 0, 0))
		pygame.draw.ellipse(s, pygame.Color(255, 255, 192, 96), pygame.Rect(0, 0, s.get_width(), s.get_height()))
		frTopLeft = (1 - frEllipse) / 2
		surface.blit(s, (w * frTopLeft, h * frTopLeft))

		for i in xrange(0,len(self.word)):
			self.drawLetter(surface,i)

	def drawLetter(self,surface,index):
		x = self.getLetterX(index)
		if index < self.charsTyped:
			h = self.doneColorHue
			color = pygame.Color(0); color.hsva = h, 100, 100, 100
			colorb = self.doneColorB
		else: color = self.notDoneColor; colorb = self.notDoneColorB

		letter = self.word[index]
		img = self.font.render(letter, True, color)
		imgb = self.boldFont.render(letter, True, colorb)
		surface.blit(imgb,imgb.get_rect(centerx = x+4, centery = self.textY))
		surface.blit(img,img.get_rect(centerx = x, centery = self.textY))

	def getLetterX(self,index):
		if len(self.word) % 2: #Odd number of letters
			x = self.textCenterX + self.letterSpacing * (index - len(self.word)/2)
		else: #Even number of letters
			x = self.textCenterX + int(round( self.letterSpacing * (index + 0.5 - len(self.word)/2) ))
		return x

	def getWordList(self,name):
		l = []
		inFile = open(os.path.join('data',name+'.txt'),'r')
		while 1:
			nextLine = inFile.readline()
			if nextLine == '': break
			else:
				nextLine = nextLine[0:len(nextLine)-1] #Remove \n at end
				l.append(nextLine)
		inFile.close()
		return l

	def getKey(self,key):
		asChar = pygame.key.name(key)
		if asChar == self.word[self.charsTyped]:
			self.getCharTypedSuccess()
		else:
			if self.loseRecoilTime == 0: #No failure if just lost.
				self.getFailure()

	def getCharTypedSuccess(self):
		x = self.getLetterX(self.charsTyped)
		y = self.textY
		self.main.explosionGraphics.getPoint(x,y)

		self.charsTyped += 1
		if self.charsTyped == len(self.word):
			self.main.getScore()
			self.resetWord()

	def getFailure(self):
		self.loseRecoilTime = self.MAX_LOSE_RECOIL_TIME
		self.charsTyped = 0
		self.main.getLose()

	def resetWord(self):
		try: oldWord = self.word
		except AttributeError: oldWord = self.word = '' #self.word not set yet

		while self.word == oldWord:
			#Store a new word to self.word
			if random.random() < self.HAPPY_WORD_CHANCE:
				self.word = self.happyWordBank[random.randint(0,len(self.happyWordBank)-1)]
			else:
				self.word = self.wordBank[random.randint(0,len(self.wordBank)-1)]

		self.charsTyped = 0 #NUMBER of characters typed in word so far.
