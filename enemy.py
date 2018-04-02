from color import *
import random
from entity import *
import pygame

class Enemy(Entity):
	# Static Variables
	enemylist = pygame.sprite.Group()
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

	def update(self):
		self.pos['x'] += self.velocity['x']
		if self.pos['x'] > winw + self.size['width'] or self.pos['x'] < 0 - self.size['width']:
			self.enemylist.remove(self)
		super().update()
	
	@classmethod # Static Method
	def reset(klass, data):
		global enemylist, spawnrate, direction
		klass.enemylist = pygame.sprite.Group()
		klass.spawnrate = data['spawnrate']
		klass.direction = data['direction']
		klass.rrange    = data['random_range']

	@classmethod # Static Method
	def difficulty(klass, data):
		global spawnrate, direction
		klass.spawnrate = data['spawnrate']
		klass.direction = data['direction']
		klass.rrange    = data['random_range']