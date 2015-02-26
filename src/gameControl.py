import os, pygame
import graphics, helpers, status, word

#Overall control of game flow.

class GameControl:
	def __init__(self,main):
		self.main = main

		self.phase = 0

		self.phase1Secs = 2*60 + 48 + - 10 #-10 for intro screens
		self.phase2Secs = 2*60 + 12 - 20./3 #-20./3 for 2nd intro screens (music plays after first)
		#2*60 + 12 is until the main song is over (sound file continues with finale during "I'M FREE!" screen.

		self.phase1Length = self.phase1Secs * self.main.FPS #In frames
		self.phase2Length = self.phase2Secs * self.main.FPS #In frames
		self.phase1Time = self.phase2Time = 0

		self.phase1MMMDecStart = 180; self.phase1MMMDecEnd = 80
		self.phase2MMMDecStart = 80; self.phase2MMMDecEnd = 80#50

	def compute(self):
		if self.phase == 1:
			self.main.status.setMMMDec(self.phase1MMMDecStart + float(self.phase1MMMDecEnd - self.phase1MMMDecStart)*self.phase1Time/self.phase1Length)
			self.phase1Time += 1
			if self.phase1Time >= self.phase1Length:
				self.startPhase2()
		else:
			self.main.status.setMMMDec(self.phase2MMMDecStart + float(self.phase2MMMDecEnd - self.phase2MMMDecStart)*self.phase2Time/self.phase2Length)
			self.phase2Time += 1
			if self.phase2Time >= self.phase2Length:
				self.winGame()

	def draw(self,surface): pass

	def start(self):
		if self.main.MUSIC_ON: helpers.playMusic('1')
		self.main.displayImageAndText('intro0','Outside?',3*self.main.FPS)
		self.main.displayImageAndText('intro1','Rescuer!',3*self.main.FPS)
		self.main.displayImageAndText('intro2','Escape!',4*self.main.FPS)

		self.startPhase1()

	def startPhase1(self):
		self.phase = 1

		self.main.get(graphics.SwimBackground(self.main))
		self.main.status = status.Status(self.main)
		self.main.get(self.main.status)
		self.main.get(word.Word(self.main))
		self.main.get(graphics.Shower(self.main))

	def startPhase2(self):
		self.phase = 2

		self.main.displayImageAndText('halfway','So close!',8*self.main.FPS)
		if self.main.MUSIC_ON: helpers.playMusic('2')
		self.main.displayImageAndText('uh-oh','Better hurry!',20./3*self.main.FPS)

		self.main.get(graphics.StarFire(self.main))
		self.main.status.clearMMM()

	def winGame(self):
		self.main.displayImageAndText('win',"I'M FREE!",12*self.main.FPS)
		if self.main.MUSIC_ON: helpers.playMusic('win')
		self.main.displayImageAndText('win2',"SCORE: " + str(self.main.status.score),-1)
