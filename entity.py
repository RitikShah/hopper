from color import *
import pygame

winw = 800
winh = 600

class Entity(pygame.sprite.Sprite):
	def __init__(self, posx, posy, velx=0, vely=0, h=5, w=5, grav=1, color=None):
		# Superclass constructor call
		super().__init__()

		self.grav 	   = grav
		self.size 	   = {'width': w, 'height': h}
		self.velocity  = {'x': velx, 'y': vely}
		self.pos	   = {'x': posx, 'y': posy - h/2}

		if color == None:
			self.color = randcolor()
		else:
			self.color = c
 
	    # Set the background color and set it to be transparent
	    self.image = pygame.Surface(self.size['width'], self.size['height'])
	    self.image.fill(white)
	    self.image.set_colorkey(white)
 
    	# Draw the box
    	pygame.draw.rect(self.image, self.color, [self.pos['x'], self.pos['y'], self.size['width'], self.size['height']])

    	# Must have, God knows
    	self.rect = self.image.get_rect()

	def __str__(self):
		return self.__class__ + ' Entity'

	def display(self):
		return [self.pos['x'], self.pos['y'], self.size['width'], self.size['height']]

	def gravity(self):
		self.pos['y'] += self.velocity['y']
		self.velocity['y'] += self.grav
		if self.pos['y'] > winh-self.floorlevel:
			self.pos['y'] = winh-self.floorlevel
			self.velocity['y'] = 0

	def update(self):
		print(self)

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
'''
	def getfloor(self):
		return floor

# Wierd :/
class Floor(Entity):
	def __init__(self):
'''