import pygame
import time
import random
import entity
from text import *
from color import *

winw = 800
winh = 600

class Game:
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.gamedisplay = pygame.display.set_mode((winw, winh))
		pygame.display.set_caption("Slayin'")

		self.fps 	   = 60
		self.crashed   = False

		self.keynone   = tuple([0] * 323)

		self.t_empty   = Text(self.gamedisplay, '')
		self.t_title   = Text(self.gamedisplay, "Slayin'", green, 100)
		self.t_over    = Text(self.gamedisplay, 'Game Over', red, 80)

		self.t_play    = Text(self.gamedisplay, 'C to play', yoffset=60)
		self.t_quit    = Text(self.gamedisplay, 'Q to quit', yoffset=80)
		self.t_back    = Text(self.gamedisplay, 'B to go back to the main menu', yoffset=100)

		self.s_main    = Screen(self.gamedisplay, self.t_title, c=self.t_play, q=self.t_quit)
		self.s_dead    = Screen(self.gamedisplay, self.t_over, c=self.t_play, q=self.t_quit, b=self.t_back)

		self.levelpoints = [
			[35, 2],
			[75, 3],
			[135, 4],
			[190, 5],
			[250, 6],
			[300, 7],
			[360, 8],
			[440, 9],
			[520, 10]
		]

		self.leveldifficulty = {
			2:  (90),
			3:  (80),
			4:  (65),
			5:  (50),
			6:  (50),
			7:  (45),
			8:  (45),
			9:  (35),
			10: (30),
		}

	def quitgame(self):
		pygame.quit()
		quit()

	def xbutton(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quitgame()

	def run(self):
		while True:
			self.level 	   = 1
			self.c 		   = entity.Character(winw/2, winh/2)
			self.tick	   = 0
			self.points    = 0
			entity.Enemy.reset()
		
			output = self.s_main.loop()
			if output == pygame.K_q:
				self.quitgame()

			exitcode = self.gameloop()

			if exitcode == 'quit':
				self.quitgame()
			elif exitcode == 'dead':
				continue
	
	
	def levelmanager(self):
		for a in self.levelpoints:
			if self.points > a[0]:
				self.level = a[1]
				entity.Enemy.spawnrate = self.leveldifficulty[self.level]
	
	def waitforrelease(self):
		pygame.event.pump()
		key = pygame.key.get_pressed()
		while not key == self.keynone:
			pygame.event.pump()
			key = pygame.key.get_pressed()
			self.clock.tick(self.fps)

	def gameloop(self):
		while not self.crashed:
			self.xbutton()

			key = pygame.key.get_pressed()
			if key[pygame.K_q]:
				self.waitforrelease()
				return 'quit'
			else:
				self.c.update(key)
				for e in entity.Enemy.enemylist:
					e.update()

			# Display Clear
			self.gamedisplay.fill(black)

			# Display Character
			pygame.draw.rect(self.gamedisplay, self.c.color, self.c.display())

			# Display Enemies
			for e in entity.Enemy.enemylist:
				pygame.draw.rect(self.gamedisplay, e.color, e.display())
				if e.iscolliding(self.c):
					return 'dead'

			if self.tick > entity.Enemy.spawnrate:
				self.tick = 0
				entity.Enemy() # new enemy

			self.tick += 1

			if self.tick % 10 == 0:
				self.points += 1

			self.levelmanager()

			# Display
			Text(self.gamedisplay, 'Level: ' + str(self.level), white, ycenter=False, yoffset=20).displaytext()
			Text(self.gamedisplay, 'Score: ' + str(self.points), white, ycenter=False, yoffset=40).displaytext()
			Text(self.gamedisplay, 'Spawn Rate: ' + str(entity.Enemy.spawnrate), white, ycenter=False, yoffset=60).displaytext()

			pygame.display.update()
			self.clock.tick(self.fps)
