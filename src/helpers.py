import math, os, pygame, random

def randomInRange(a,b): return a + random.random()*(b - a)
def randHSV(): c = pygame.color.Color(0); c.hsva = (randomInRange(0,360),100,100,100); return c

def loadPNG(name, colorkey=None):
	#Loads any PNG, automatically formatting for transparancy/colorkey and converting image to fastest format
	fullname = os.path.join('data', 'images', name+'.png')
	if colorkey is None: #Treat it as an image with transparency
		image = pygame.image.load(fullname).convert_alpha()
	else:
		image = pygame.image.load(fullname).convert()
		if colorkey == -1: colorkey = image.get_at((0,0))
		image = image.convert()
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image, image.get_rect()

def loadPNGPlain(name):
	#Loads a PNG, no alpha, no colorkey
	fullname = os.path.join('data', 'images', name+'.png')
	image = pygame.image.load(fullname).convert()
	return image, image.get_rect()

def playMusic(name,loops=0):
	pygame.mixer.music.stop()
	pygame.mixer.music.load(os.path.join('data','music',name+'.ogg'))
	pygame.mixer.music.play(loops)

def playSound(name,volumeMult=1):
	'''Plays a sound effect once.'''
	normVol = 1; volume = normVol*volumeMult
	fullname = os.path.join('data','sounds',name+'.wav')
	try:
		sound = pygame.mixer.Sound(fullname)
		sound.set_volume(volume)
		sound.play()
	except pygame.error, message:
		print 'Cannot load sound:', fullname
		raise SystemExit, message

class Oscillator:
	def __init__(self,sinSpeed,minimum=-1,maximum=1):
		self.sinx = 0
		self.sinSpeed = sinSpeed
		self.center = float(maximum+minimum)/2; self.amp = float(maximum-minimum)/2
		self.value = self.center

	def compute(self):
		self.sinx += self.sinSpeed
		if self.sinx > math.pi: self.sinx -= 2*math.pi
		self.value = self.center + self.amp*math.sin(self.sinx)

	def getValue(self): return self.value
	def setSpeed(self,sinSpeed): self.sinSpeed = sinSpeed
