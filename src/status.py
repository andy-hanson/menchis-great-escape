import math, os, pygame
import helpers

class Status:
	def __init__(self,main):
		self.main = main
		self.drawPriority = 1

		self.score = 0

		self.fontSize = int(round(self.main.FIELD_HEIGHT*0.3))
		self.font = pygame.font.Font(os.path.join('data', 'font', 'scoreFont.ttf'), self.fontSize)
		self.fontHue = 0; self.fontHueChange = 1

		#Menchi Munchie Meter: If it gets too high, you lose!
		self.MMMMax = 1000
		self.MMM = 0
		self.MMMInc = 1 #Per frame
		self.MMMDec = 150 #When score. Change THIS to make the game harder. Min about 50.

		self.MMMBarWidth = self.main.FIELD_WIDTH
		self.MMMBarLeft = self.main.FIELD_WIDTH - self.MMMBarWidth
		self.MMMBarHeight = self.main.FIELD_HEIGHT
		self.MMMBarMaxY = self.main.FIELD_HEIGHT
		#MMMBar varies in color, saturation.
		self.SAFE_HUE = 300
		self.DEAD_HUE = 0
		self.MMMSatOsc = helpers.Oscillator(0,50,100)
		self.MMMSatOscSafeSpeed = math.pi/240
		self.MMMSatOscDeadSpeed = math.pi/10

	def compute(self):
		self.MMMMove(self.MMMInc)
		if self.MMM == self.MMMMax and self.main.CAN_LOSE:
			self.main.getGameOver()

		self.fontHue += self.fontHueChange
		if self.fontHue >= 360: self.fontHue -= 360

		self.MMMSatOsc.compute()
		self.MMMSatOsc.setSpeed(self.MMMSatOscSafeSpeed + float(self.MMMSatOscDeadSpeed - self.MMMSatOscSafeSpeed) * self.MMM/self.MMMMax)

	def draw(self,surface):
		#Draw Menchi Munchie Meter
		hue = self.SAFE_HUE + float(self.DEAD_HUE-self.SAFE_HUE) * self.MMM/self.MMMMax
		vel = 100; sat = self.MMMSatOsc.getValue(); alpha = 100
		color = pygame.Color(0); color.hsva = hue, sat, vel, alpha
		thisHeight = self.MMMBarHeight * self.MMM/self.MMMMax
		r = pygame.Rect(self.MMMBarLeft, self.MMMBarMaxY-thisHeight, self.MMMBarWidth, thisHeight)
		pygame.draw.rect(surface,color,r)

		#Draw score
		hue = self.fontHue; vel = 100; sat = 100; alpha = 50
		color = pygame.Color(0); color.hsva = hue, sat, vel, alpha
		text = self.font.render(str(self.score),1,color)
		surface.blit(text,text.get_rect(centerx=self.main.FIELD_WIDTH/2,top=0))

	def getScore(self):
		helpers.playSound('getWord')
		self.score += 1
		self.MMMMove(-self.MMMDec)

	def getLose(self):
		self.score -= 1

	def MMMMove(self,amount):
		#Increase self.MMM by amount
		self.MMM += amount
		if self.MMM > self.MMMMax:
			self.MMM = self.MMMMax
		elif self.MMM < 0:
			self.MMM = 0

	def setMMMDec(self,amount): self.MMMDec = amount
	def clearMMM(self): self.MMM = 0
