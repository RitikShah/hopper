import pygame
import json
import time
import random
from enemy import *
from character import *
from text import *
from screen import *
from color import *

winw = 800
winh = 600

class Game:
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.gamedisplay = pygame.display.set_mode((winw, winh))
		pygame.display.set_caption("Hopper")

		with open('level.json') as file:
			self.data = json.load(file)

		self.fps 	   = 60
		self.crashed   = False

		self.keynone   = tuple([0] * 323)

		self.t_empty   = Text(self.gamedisplay, '')
		self.t_title   = Text(self.gamedisplay, "Hopper", green, 100)
		self.t_over    = Text(self.gamedisplay, 'Game Over', red, 80)

		self.t_play    = Text(self.gamedisplay, 'C to play', yoffset=60)
		self.t_quit    = Text(self.gamedisplay, 'Q to quit', yoffset=80)
		self.t_back    = Text(self.gamedisplay, 'B to go back to the main menu', yoffset=100)

		self.s_main    = Screen(self.gamedisplay, self.t_title, c=self.t_play, q=self.t_quit)

		self.player	   = Character(winw/2, winh/2)

	def curve(self, currentlevel):
		return (currentlevel**1.2) * 30

	def quitgame(self):
		pygame.quit()
		quit()

	def xbutton(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quitgame()

	def run(self):
		output = self.s_main.loop()
		while True:
			self.level 	    = 1
			self.tick	    = 0
			self.points     = 0
			self.player.reset(winw/2, winh/2)

			self.allsprites = pygame.sprite.Group()
			self.allsprites.add(self.player)

			Enemy.reset(self.data[0])
		
			if output == pygame.K_q:
				self.quitgame()

			exitcode = self.gameloop()

			if exitcode == 'quit':
				self.quitgame()
			elif exitcode == 'dead':
				output = self.gameover()
	
	def gameover(self):
		s_gameover = Screen(self.gamedisplay, self.t_over, Text(self.gamedisplay, 'Level: ' + str(self.level), yoffset=20, ycenter=False), Text(self.gamedisplay, 'Score: ' + str(self.points), yoffset=40, ycenter=False),c=self.t_play, q=self.t_quit, b=self.t_back)
		return s_gameover.loop()

	def levelmanager(self):
		if self.points > self.curve(self.level):
			self.level += 1
			if len(self.data) >= self.level:
				Enemy.difficulty(self.data[self.level - 1])
			# later: Include infinite difficulty curve

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

			# Key Listeners
			key = pygame.key.get_pressed()
			if key[pygame.K_q]:
				self.waitforrelease()
				return 'quit'
			elif key[pygame.K_p]:
				Text(self.gamedisplay, '~ Paused ~', white, 60).displaytext()
				pygame.display.update()
				self.waitforrelease()
				key = pygame.key.get_pressed()
				while not(key[pygame.K_p]):
					self.xbutton()
					key = pygame.key.get_pressed()
				self.waitforrelease()
			else:
				self.player.update(key)
				Enemy.enemylist.update()

			# Collision Detection 
			collisions = pygame.sprite.spritecollide(self.player, Enemy.enemylist, True)
			if len(collisions) > 1:
				return 'dead'

			# Enemy Spawning
			if self.tick > Enemy.spawnrate:
				self.tick = 0
				enemy = Enemy() # new enemy
				Enemy.enemylist.add(enemy)
				self.allsprites.add(enemy)

			self.tick += 1

			if self.tick % 10 == 0:
				self.points += 1

			self.levelmanager()

			# Display Clear
			self.gamedisplay.fill(black)

			# Draw all sprites
			self.allsprites.draw(self.gamedisplay)

			# Display Enemies
			#for e in Enemy.enemylist:
			#	pygame.draw.rect(self.gamedisplay, e.color, e.display())
			#	if e.iscolliding(self.player):
			#		return 'dead'

			# Display Floor
			# pygame.draw.rect(self.gamedisplay, white, [0, winh-95, winw, 4])

			# Display Text (last two temp)
			Text(self.gamedisplay, 'Level: ' + str(self.level), white, ycenter=False, yoffset=20).displaytext()
			Text(self.gamedisplay, 'Score: ' + str(self.points), white, ycenter=False, yoffset=40).displaytext()
			Text(self.gamedisplay, 'Spawn Rate: ' + str(Enemy.spawnrate), white, ycenter=False, yoffset=60).displaytext()
			Text(self.gamedisplay, 'Direction: ' + str(Enemy.direction), white, ycenter=False, yoffset=80).displaytext()

			# Update and tick @ 60fps
			pygame.display.flip()
			self.clock.tick(self.fps)
