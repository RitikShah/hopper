from color import *
import random
import pygame

winw = 800
winh = 600

class Entity:
	def __init__(self, px, py, vx=0, vy=0, h=5, w=5, c=None):
		self.size 		= {'height': h, 'width': w}
		self.velocity	= {'x': vx, 'y': vy}
		self.pos		= {'x': px, 'y': py - h/2}

		if c == None:
			self.color 	= randcolor()
		else:
			self.color	= c

	def display(self):
		return [self.pos['x'], self.pos['y'], self.size['width'], self.size['height']]

	def iscolliding(self, entity):
		# self corners
		if self.pos['x'] + self.size['width']/2 > entity.pos['x'] - entity.size['width']/2 and self.pos['x'] + self.size['width']/2 < entity.pos['x'] + entity.size['width']/2:
			if self.pos['y'] + self.size['height']/2 > entity.pos['y'] - entity.size['height']/2 and self.pos['y'] + self.size['height']/2 < entity.pos['y'] + entity.size['height']/2:
				return True
			elif self.pos['y'] - self.size['height']/2 < entity.pos['y'] + entity.size['height']/2 and self.pos['y'] - self.size['height']/2 > entity.pos['y'] - entity.size['height']/2:
				return True
		if self.pos['x'] - self.size['width']/2 < entity.pos['x'] + entity.size['width']/2 and self.pos['x'] - self.size['width']/2 > entity.pos['x'] - entity.size['width']/2:
			if self.pos['y'] + self.size['height']/2 > entity.pos['y'] - entity.size['height']/2 and self.pos['y'] + self.size['height']/2 < entity.pos['y'] + entity.size['height']/2:
				return True
			elif self.pos['y'] - self.size['height']/2 < entity.pos['y'] + entity.size['height']/2 and self.pos['y'] - self.size['height']/2 > entity.pos['y'] - entity.size['height']/2:
				return True
		else:
			return False

class Enemy(Entity):
	def __init__(self):
		if random.randint(0,1) == 1:
			vx = random.randint(1,4)
			px = 0
		else:
			vx = -random.randint(1,10)	
			px = winw

		super().__init__(px, winh-100, vx, 0, random.randint(5,20), random.randint(5,20))

	def update(self):
		self.pos['x'] += self.velocity['x']
		if self.pos['x'] > winh + self.size['width'] or self.pos['x'] < 0 - self.size['width']:
			del self

class Character(Entity):
	def __init__(self, px, py):
		super().__init__(px, py)

		self.grav = 1

	def update(self, key):
		# Key Listener
		if key[pygame.K_SPACE] and self.pos['y'] == winh-100: # jump
			self.velocity['y'] = -10
		if key[pygame.K_LEFT]:
			self.pos['x'] -= 5
		elif key[pygame.K_RIGHT]:
			self.pos['x'] += 5	

		# Gravity
		self.pos['y'] += self.velocity['y']
		self.velocity['y'] += self.grav
		if self.pos['y'] > winh-100:
			self.pos['y'] = winh-100
			self.velocity['y'] = 0