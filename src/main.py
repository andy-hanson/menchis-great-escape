import pygame
import gameControl, graphics, helpers

class Main:
	'''This is the "hub" class.'''
	def __init__(self):
		self.FIELD_WIDTH = 800
		self.FIELD_HEIGHT = 600
		self.rect = pygame.Rect(0,0,self.FIELD_WIDTH,self.FIELD_HEIGHT)
		self.drawScreen = pygame.display.set_mode((self.FIELD_WIDTH,self.FIELD_HEIGHT))

		self.clock = pygame.time.Clock()
		self.FPS = 50

		pygame.init()

		self.SPECIAL_EFFECTS_ON = 1
		self.MUSIC_ON = 1
		self.CAN_LOSE = 1 #Turn this off and game over never happens!

		self.clearObjects()

		self.gameControl = gameControl.GameControl(self)
		self.get(self.gameControl)

		self.explosionGraphics = graphics.ExplosionGraphics(self); self.get(self.explosionGraphics)

	def run(self):
		self.gameRunning = 1

		self.gameControl.start()

		while self.gameRunning:
			self.draw()
			pygame.display.set_caption("Menchi's Great Escape August 1 2010 - FPS " + str(int(self.clock.get_fps())) + '/' + str(self.FPS))
			self.clock.tick(self.FPS)
			self.getInput()
			self.compute()

		pygame.quit()

	def getInput(self):
		for event in pygame.event.get():
			#React to the event. You could call object functions every time an event happens, or you could store pressed keys as a variable.
			if event.type == pygame.QUIT:   #Good idea to also have escape key quitting, especially in fullscreen games or ones that use the mouse in odd ways.
				self.gameRunning = 0 #For now we'll leave it simple and just shut off immediately.

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN: #Enter
					pass
				elif (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_CAPSLOCK).count(event.key):
					pass #No punishment for pressing these keys
				else:
					for o in self.objects:
						hasFunction = 0
						try: o.getKey; hasFunction = 1
						except AttributeError: hasFunction = 0
						if hasFunction: o.getKey(event.key)

	def compute(self):
		index = 0
		while index < len(self.objects):
			self.objects[index].compute()
			#When you want to destroy an object, just give it a new variable, "dead", and set it to true.
			if self.objects[index].dead:
				self.objects.remove(self.objects[index])
				index -= 1
			index += 1

	def draw(self):
		for drawPriority in xrange(self.MIN_DRAW_PRIORITY,self.MAX_DRAW_PRIORITY+1):
			for obj in self.byDrawPriority[drawPriority]:
				obj.draw(self.drawScreen)
		pygame.display.flip()

	def clearObjects(self):
		self.objects = []
		self.byType = {} #Dictionary sorting objects by their class
		self.MIN_DRAW_PRIORITY = -2; self.MAX_DRAW_PRIORITY = 4

		#-2: Swimming background
		#-1: ???
		#0: Shower
		#1: Status
		#2: The word
		#3: Explosions
		self.byDrawPriority = {-2:[], -1:[], 0:[], 1:[], 2:[], 3:[], 4: []} #Dictionary sorting objects by their draw priority. DON'T ADD ANY NEW KEYS!


	def get(self,obj):
		self.objects.append(obj)
		try: obj.drawPriority
		except AttributeError: obj.drawPriority = 0
		try:
			obj.dead
			if obj.dead == 0:
				print('ERROR: ' + str(obj) + ' has dead already set to 0!')
		except AttributeError: obj.dead = 0
		#Insert it into byType and byDrawPriority
		try: self.byType[obj.__class__].append(obj)
		except KeyError: self.byType[obj.__class__] = [obj]
		self.byDrawPriority[obj.drawPriority].append(obj)

	def getScore(self):
		for o in self.objects:
			try: o.getScore; hasFunction = 1
			except AttributeError: hasFunction = 0
			if hasFunction: o.getScore()

	def getLose(self): #When miss a word
		self.status.getLose()

	def getGameOver(self):
		if self.MUSIC_ON: helpers.playMusic('game over')
		self.displayImageAndText('game over','GAME OVER',8*self.FPS)
		self.displayImageAndText('game over2','Score: ' + str(self.status.score),-1)

	def displayImageAndText(self,imageName,text,time):
		#If negative time, lasts forever
		image = helpers.loadPNGPlain(imageName)[0]
		image = pygame.transform.smoothscale(image,self.rect.size)
		if time > 0: buildUpTime = time/2
		else: buildUpTime = 240
		textMover = graphics.TextMover(self,buildUpTime,text)

		t = 0
		while (time < 0 or t < time) and self.gameRunning:
			t += 1

			self.clock.tick(self.FPS)

			self.drawScreen.blit(image,(0,0))
			textMover.compute(); textMover.draw(self.drawScreen)
			pygame.display.flip()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.gameRunning = 0

			pygame.display.set_caption(text)


Main().run()
