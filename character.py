from color import *
import random
from entity import *
import pygame

class Character(Entity):
	def __init__(self, posx, posy):
		super().__init__(posx, posy, 5)
		self.grav  		= 1
		self.xspeed		= 5
		self.floorlevel = 100

		self.jumpheight = 15
		self.jumps 		= 0
		self.maxjumps	= 1
		self.spacehold  = False

	def update(self, key):
		# Key Listener
		if key[pygame.K_SPACE] and not(self.spacehold):
			if self.pos['y'] == winh-self.floorlevel: 	# Ground Level
				self.jumps = self.maxjumps
				self.velocity['y'] = -self.jumpheight
				self.spacehold = True
			elif self.jumps > 0:						# Double Jump
				self.jumps -= 1
				self.velocity['y'] = -self.jumpheight
				self.spacehold = True
		elif not(key[pygame.K_SPACE]):
			self.spacehold = False

		if key[pygame.K_LEFT]:
			self.pos['x'] -= self.xspeed
		elif key[pygame.K_RIGHT]:
			self.pos['x'] += self.xspeed

		if self.pos['x'] > winw-self.size['width']:
			self.pos['x'] = winw-self.size['width']
		if self.pos['x'] < 0:
			self.pos['x'] = 0

		# Gravity
		self.pos['y'] += self.velocity['y']
		self.velocity['y'] += self.grav
		if self.pos['y'] > winh-self.floorlevel:
			self.pos['y'] = winh-self.floorlevel
			self.velocity['y'] = 0

	def reset(self, posx, posy):
		self.__init__(posx, posy)
		