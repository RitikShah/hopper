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

	def quitgame(self):
		pygame.quit()
		quit()

	def xbutton(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quitgame()

	def newgame(self):
		self.level 	   = 1
		self.c 		   = entity.Character(winw/2, winh/2)
		self.tick	   = 0

		while True:
			output = self.s_main.loop()
			if output == pygame.K_q:
				self.quitgame()

			exitcode = self.gameloop()

			if exitcode == 'q':
				self.quitgame()
			elif exitcode == 'd':
				self.newgame()

	def waitforrelease(self):
		pygame.event.pump()
		key = pygame.key.get_pressed()
		while not key == self.keynone:
			pygame.event.pump()
			key = pygame.key.get_pressed()
			self.clock.tick(self.fps)

	def gameloop(self):
		enemylist = []
		while not self.crashed:
			self.xbutton()

			key = pygame.key.get_pressed()
			if key[pygame.K_q]:
				self.waitforrelease()
				return 'q'
			else:
				self.c.update(key)
				for e in enemylist:
					e.update()

			# Display Clear
			self.gamedisplay.fill(black)

			# Display Character
			pygame.draw.rect(self.gamedisplay, self.c.color, self.c.display())

			# Display Enemies
			for e in enemylist:
				pygame.draw.rect(self.gamedisplay, e.color, e.display())
				if e.iscolliding(self.c):
					return 'd'

			if self.tick > 100:
				self.tick = 0
				enemylist.append(entity.Enemy())

			self.tick += 1

			pygame.display.update()
			self.clock.tick(self.fps)
