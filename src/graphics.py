import math, os, pygame, random
import helpers
import PyIgnition

# TODO: Duplicate code in word.py
class TextMover:
	def __init__(self,main,buildUpTime,text):
		self.main = main
		self.text = text

		self.letterSpacing = self.main.FIELD_WIDTH/(len(self.text)+1)
		self.fontSize = int(self.letterSpacing * 1.5)
		self.boldFontSize = int(self.letterSpacing * 1.6)

		self.font = pygame.font.Font(os.path.join('data', 'font', 'wordFont.ttf'), self.fontSize)
		self.boldFont = pygame.font.Font(os.path.join('data', 'font', 'wordFontB.ttf'), self.boldFontSize)
		self.boldFont.set_bold(True)
		self.fontColor = (255, 255, 255)
		self.fontColorB = (0, 0, 0)

		#Gradually fill in letters
		self.usedLetters = 0
		self.buildUpTime = int(round(buildUpTime))
		self.time = 0

		self.textCenterX = self.main.FIELD_WIDTH/2
		self.textY = self.main.FIELD_HEIGHT/2

	def compute(self):
		self.time += 1
		self.usedLetters = len(self.text) * self.time / self.buildUpTime
		if self.usedLetters > len(self.text): self.usedLetters = len(self.text)

	def draw(self,surface):
		for i in xrange(self.usedLetters):
			self.drawLetter(surface,i)
		#text = self.font.render(thisString,1,self.fontColor)
		#surface.blit(text,text.get_rect(center=self.main.rect.center))
		#text = self.boldFont.render(thisString,1,self.fontColor)
		#surface.blit(text,text.get_rect(center=self.main.rect.center))

	def drawLetter(self,surface,index):
		x = self.getLetterX(index)
		if index < self.usedLetters:
			letter = self.text[index]
			img = self.font.render(letter,1,self.fontColor)
			imgb = self.boldFont.render(letter,1,self.fontColorB)
			surface.blit(imgb,imgb.get_rect(centerx = x+4, centery = self.textY))
			surface.blit(img,img.get_rect(centerx = x, centery = self.textY))

	def getLetterX(self,index):
		if len(self.text) % 2: #Odd number of letters
			x = self.textCenterX + self.letterSpacing * (index - len(self.text)/2)
		else: #Even number of letters
			x = self.textCenterX + int(round( self.letterSpacing * (index + 0.5 - len(self.text)/2) ))
		return x

class SwimBackground:
	def __init__(self,main):
		self.main = main
		self.drawPriority = -2

		self.NUM_FRAMES = 6
		self.animation = []
		for i in xrange(self.NUM_FRAMES):
			img = helpers.loadPNGPlain(os.path.join('swim animation',str(i)))[0]
			img = pygame.transform.smoothscale(img,self.main.rect.size)

			self.animation.append(img)

		self.imageIndex = 0
		self.image = self.animation[0]

		#Doggie time is different than the frames.
		self.DOGGIE_TIME_BETWEEN_IMAGES = 100 #Don't change this!
		self.doggieTimeSpeed = 10 #Amount doggie time advances per frame. Can change this.
		self.doggieTime = 0

		self.MIN_DOGGIE_TIME_SPEED = 10
		self.MAX_DOGGIE_TIME_SPEED = 30 #Set to this hen get score.
		self.DOGGIE_TIME_SPEED_DEC = 0.125 #Every frame, slowly reducing to minimum

	def compute(self):
		if self.doggieTimeSpeed > self.MIN_DOGGIE_TIME_SPEED:
			self.doggieTimeSpeed -= self.DOGGIE_TIME_SPEED_DEC

		self.doggieTime += self.doggieTimeSpeed
		if self.doggieTime >= self.DOGGIE_TIME_BETWEEN_IMAGES:
			self.doggieTime -= self.DOGGIE_TIME_BETWEEN_IMAGES
			self.imageIndex += 1
			if self.imageIndex >= self.NUM_FRAMES: self.imageIndex = 0
			self.image = self.animation[self.imageIndex]

	def draw(self,surface):
		surface.blit(self.image,(0,0))

	def getScore(self):
		self.doggieTimeSpeed = self.MAX_DOGGIE_TIME_SPEED

class ExplosionGraphics:
	def __init__(self,main):
		self.main = main
		self.drawPriority = 3

		self.explosionLastTime = 30 #Of image part
		self.explosionPoints = [] #X,Y,Time,minRad,maxRad
		self.explosionImage = helpers.loadPNG('explosion')[0]
		self.xScroll = 0
		self.yScroll = 0

		self.particleEffect = PyIgnition.ParticleEffect(self.main.drawScreen,(0,0),self.main.drawScreen.get_size())
		self.particleSource = self.particleEffect.CreateSource((0,0),initdirection=0.0,initdirectionrandrange = math.pi, particlesperframe = 0, \
														  particlelife = 30, drawtype = PyIgnition.DRAWTYPE_LINE, colour = (255,255,255), length=8.0)

		self.particleSource.CreateParticleKeyframe(10,colour=(255,0,0))
		self.particleSource.CreateParticleKeyframe(20,colour=(0,255,0))
		self.particleSource.CreateParticleKeyframe(30,colour=(0,0,255))
		self.particlesEmitTime = 1 #How long to emit particles after an explosion.

		#Lift on particles
		'''strength = 0.20
		strengthrandrange = 0;
		gravity = self.particleEffect.CreateDirectedGravity(strength, strengthrandrange, (0,-1))'''

		'''#Wind on particles
		strength = 0
		strengthrandrange = 2.0
		wind = self.particleEffect.CreateDirectedGravity(strength, strengthrandrange, (1,0))'''

	def compute(self):
		if self.main.SPECIAL_EFFECTS_ON:
			i = 0
			while i < len(self.explosionPoints):
				self.explosionPoints[i][0] += self.xScroll; self.explosionPoints[i][1] += self.yScroll
				self.explosionPoints[i][2] -= 1
				if self.explosionPoints[i][2] == 0:
					self.explosionPoints.remove(self.explosionPoints[i])
					i -= 1
				i += 1

			self.particleEffect.Update()

	def draw(self,surface):
		if self.main.SPECIAL_EFFECTS_ON:
			for p in self.explosionPoints:
				minRad = p[3]; maxRad = p[4]
				thisRad = minRad + (maxRad-minRad)*(self.explosionLastTime - p[2])/self.explosionLastTime
				scaledImage = pygame.transform.smoothscale(self.explosionImage,(thisRad*2,thisRad*2))

				r = pygame.Rect(p[0]-thisRad,p[1]-thisRad,thisRad*2,thisRad*2)
				if r.colliderect(surface.get_rect()): #If it collides at all:
					r2 = r.clip(surface.get_rect())
					blitpos = r.left - r2.left, r.top - r2.top

					tempSurface = surface.subsurface(r2).copy()
					tempSurface.blit(scaledImage,blitpos)
					a = 255*p[2]/self.explosionLastTime
					tempSurface.set_alpha(a)
					surface.blit(tempSurface,r2.topleft)

			self.particleEffect.Redraw()

	def getPoint(self,x,y='isTuple',minRad=0,maxRad=100,size='small'):
		if y == 'isTuple': y = x[1]; x = x[0]
		self.explosionPoints.append([x,y,self.explosionLastTime - 1,minRad,maxRad])

		self.particleSource.ConsolidateKeyframes()
		self.particleSource.SetPos((x,y))
		if size == 'small':
			self.particleSource.SetInitSpeed(6.0); self.particleSource.SetInitSpeedRandRange(4.0)
			self.particleSource.SetParticlesPerFrame(10)

		elif size == 'big':
			self.particleSource.SetInitSpeed(6.0); self.particleSource.SetInitSpeedRandRange(4.0)
			self.particleSource.SetParticlesPerFrame(40)
		elif size == 'veryBig':
			self.particleSource.SetInitSpeed(8.0); self.particleSource.SetInitSpeedRandRange(6.0)
			self.particleSource.SetParticlesPerFrame(80)
		self.particleSource.CreateKeyframe(frame = self.particleSource.curframe + self.particlesEmitTime, particlesperframe = 0)

	def getPointBig(self,x,y='isTuple'):
		if y == 'isTuple': self.getPoint(x[0],x[1],200,400,'big')
		else: self.getPoint(x,y,100,300,'big')
	def getPointVeryBig(self,x,y='isTuple'):
		if y == 'isTuple': self.getPoint(x[0],x[1],300,600,'veryBig')
		else: self.getPoint(x,y,200,800,'veryBig')

	def useGravity(self,strength=0.25):
		strengthrandrange = 0; direction = math.pi/2
		gravity = self.particleEffect.CreateDirectedGravity(strength, strengthrandrange, (0,1))

	def setNoBlack(self):
		'''Particles will die after turning red.'''
		self.particleSource = self.particleEffect.CreateSource((0,0),initdirection=0.0,initdirectionrandrange = math.pi, particlesperframe = 0, \
														  particlelife = 20, drawtype = PyIgnition.DRAWTYPE_LINE, colour = (255,255,255), length=8.0)

		self.particleSource.CreateParticleKeyframe(10,colour=(255,255,0))
		self.particleSource.CreateParticleKeyframe(20,colour=(255,0,0))

class Shower:
	def __init__(self,main):
		self.main = main
		self.drawPriority = 0

		position = (self.main.FIELD_WIDTH/2, -300)

		angToCorner = math.atan2(300,self.main.FIELD_WIDTH/2)

		self.particleEffect = PyIgnition.ParticleEffect(self.main.drawScreen,(0,0),self.main.drawScreen.get_size())
		self.particleSource = self.particleEffect.CreateSource(
			position,
			initdirection = math.pi,
			initdirectionrandrange = math.pi/2 - angToCorner,
			particlesperframe = 2, particlelife = 100,
			initspeed = 5, initspeedrandrange = 4,
			drawtype = PyIgnition.DRAWTYPE_BUBBLE, colour = (255,255,255), radius=3)#, length=8.0)


		#self.particleSource.CreateParticleKeyframe(20,colour=(255,0,0))
		#self.particleSource.CreateParticleKeyframe(40,colour=(0,255,0))
		#self.particleSource.CreateParticleKeyframe(60,colour=(0,0,255))

		#Falling
		#strength = 0.1
		#strengthrandrange = 0;
		#gravity = self.particleEffect.CreateDirectedGravity(strength, strengthrandrange, (0,1))

	def compute(self):
		if self.main.SPECIAL_EFFECTS_ON:
			self.particleEffect.Update()

	def draw(self,surface):
		if self.main.SPECIAL_EFFECTS_ON:
			self.particleEffect.Redraw()


class StarFire:
	def __init__(self,main):
		self.main = main
		self.drawPriority = 0

		self.MIN_Z_SPEED = 1
		self.Z_SPEED_INC = 1 #When get points
		self.Z_SPEED_DEC = 0.015 #Every frame
		self.Z_SPEED = self.MIN_Z_SPEED

		self.eyeDistFromScreen = 20;
		self.STAR_FADE_RAD = 75; #Radius at which opacity is 100%; then fades out by inverse square
		self.DRAW_RADIUS = 3;
		self.SPARKLE_CHANCE = 0.08;

		self.stars = []
		self.newStarChance = 0.25

	def compute(self):
		if random.random() < self.newStarChance:
			self.getNew()

		for star in self.stars:
			star.compute()

		if self.Z_SPEED > self.MIN_Z_SPEED: self.Z_SPEED -= self.Z_SPEED_DEC

	def draw(self,surface):
		for star in self.stars:
			star.draw(surface)

	def getNew(self):
		r = self.main.FIELD_WIDTH
		ang = random.random()*math.pi*2
		self.stars.append(Star(self,r*math.cos(ang),r*math.sin(ang)))

	def getScore(self):
		self.Z_SPEED += self.Z_SPEED_INC

class Star:
	def __init__(self,starFire,x,y):
		self.starFire = starFire; self.main = self.starFire.main

		self.x, self.y = x,y #x and y relative to screen center.
		self.color = helpers.randHSV()
		self.z = 250.0

	def compute(self):
		self.z -= self.starFire.Z_SPEED
		if self.z <= 0: self.dead = 1

	def draw(self,surface):
		if self.z > 0:
			color = self.color
			if random.random() < self.starFire.SPARKLE_CHANCE: color = (255,255,255)

			alpha = 255 * 1/((self.z/self.starFire.STAR_FADE_RAD)**2)
			if alpha > 255: alpha = 255
			if alpha < 0: alpha = 0
			convX = int(round( self.main.FIELD_WIDTH/2  + self.x*(self.starFire.eyeDistFromScreen/(self.starFire.eyeDistFromScreen+self.z)) ))
			convY = int(round( self.main.FIELD_HEIGHT/2 + self.y*(self.starFire.eyeDistFromScreen/(self.starFire.eyeDistFromScreen+self.z)) ))
			pygame.draw.circle(surface,color,(convX,convY),self.starFire.DRAW_RADIUS,1)
