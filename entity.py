from color import *
import random
import pygame

winw = 800
winh = 600

class Entity:
	def __init__(self, posx, posy, velx=0, vely=0, h=5, w=5, c=None):
		self.size 		= {'height': h, 'width': w}
		self.velocity	= {'x': velx, 'y': vely}
		self.pos		= {'x': posx, 'y': posy - h/2}

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
		elif self.pos['x'] - self.size['width']/2 < entity.pos['x'] + entity.size['width']/2 and self.pos['x'] - self.size['width']/2 > entity.pos['x'] - entity.size['width']/2:
			if self.pos['y'] + self.size['height']/2 > entity.pos['y'] - entity.size['height']/2 and self.pos['y'] + self.size['height']/2 < entity.pos['y'] + entity.size['height']/2:
				return True
			elif self.pos['y'] - self.size['height']/2 < entity.pos['y'] + entity.size['height']/2 and self.pos['y'] - self.size['height']/2 > entity.pos['y'] - entity.size['height']/2:
				return True
		elif entity.pos['x'] + entity.size['width']/2 > self.pos['x'] - self.size['width']/2 and entity.pos['x'] + entity.size['width']/2 < self.pos['x'] + self.size['width']/2:
			if entity.pos['y'] + entity.size['height']/2 > self.pos['y'] - self.size['height']/2 and entity.pos['y'] + entity.size['height']/2 < self.pos['y'] + self.size['height']/2:
				return True
			elif entity.pos['y'] - entity.size['height']/2 < self.pos['y'] + self.size['height']/2 and entity.pos['y'] - entity.size['height']/2 > self.pos['y'] - self.size['height']/2:
				return True
		elif entity.pos['x'] - entity.size['width']/2 < self.pos['x'] + self.size['width']/2 and entity.pos['x'] - entity.size['width']/2 > self.pos['x'] - self.size['width']/2:
			if entity.pos['y'] + entity.size['height']/2 > self.pos['y'] - self.size['height']/2 and entity.pos['y'] + entity.size['height']/2 < self.pos['y'] + self.size['height']/2:
				return True
			elif entity.pos['y'] - entity.size['height']/2 < self.pos['y'] + self.size['height']/2 and entity.pos['y'] - entity.size['height']/2 > self.pos['y'] - self.size['height']/2:
				return True
		else:
			return False

class Enemy(Entity):
	# Static Variables
	enemylist = []
	spawnrate = 100
	direction = 'l'
	rrange    = (1,5)

	def __init__(self):
		if self.direction == 'l':
			velx = random.randint(self.rrange[0],self.rrange[1])	
			posx = 0
		elif self.direction == 'r':
			velx = -random.randint(self.rrange[0],self.rrange[1])
			posx = winw
		elif self.direction == 'lr':
			if random.randint(0,1):
				velx = random.randint(self.rrange[0],self.rrange[1])
				posx = 0
			else:
				velx = -random.randint(self.rrange[0],self.rrange[1])	
				posx = winw

		super().__init__(posx, winh-100, velx, 0, random.randint(5,10), random.randint(5,10))
		self.enemylist.append(self)

	def update(self):
		self.pos['x'] += self.velocity['x']
		if self.pos['x'] > winw + self.size['width'] or self.pos['x'] < 0 - self.size['width']:
			self.enemylist.remove(self)
	
	@classmethod # Static Method
	def reset(klass):
		global enemylist, spawnrate, direction
		klass.enemylist = []
		klass.spawnrate = 100
		klass.direction = 'l'
		klass.rrange    = (1,5)

class Character(Entity):
	def __init__(self, posx, posy):
		super().__init__(posx, posy, 5)

		self.grav   = 1
		self.xspeed = 5

		self.jumpheight = 15
		self.floorlevel = 100

		self.doublejump = False
		self.spacehold  = False

	def update(self, key):
		# Key Listener
		if key[pygame.K_SPACE] and not(self.spacehold):
			if self.pos['y'] == winh-self.floorlevel: 	# Ground Level
				self.doublejump = True
				self.velocity['y'] = -self.jumpheight
				self.spacehold = True
			elif self.doublejump:						# Double Jump
				self.doublejump = False
				self.velocity['y'] = -self.jumpheight
				self.spacehold = True
		elif not(key[pygame.K_SPACE]):
			self.spacehold = False

		if key[pygame.K_LEFT]:
			self.pos['x'] -= self.xspeed
		elif key[pygame.K_RIGHT]:
			self.pos['x'] += self.xspeed

		# Gravity
		self.pos['y'] += self.velocity['y']
		self.velocity['y'] += self.grav
		if self.pos['y'] > winh-self.floorlevel:
			self.pos['y'] = winh-self.floorlevel
			self.velocity['y'] = 0