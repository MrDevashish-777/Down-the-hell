import pygame 
from Utils import * 

class HellSteps(pygame.sprite.Sprite):
	image = None

	def __init__(self, location):
		pygame.sprite.Sprite.__init__(self)

		if HellSteps.image is None:
			HellSteps.image = load_image("hellsteps.jpg")
		
		self.image = HellSteps.image

		self.rect = self.image.get_rect()
		self.rect.topleft = location
