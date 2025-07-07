import pygame

from code.Const import COLOR_RED


class Laser(pygame.sprite.Sprite):
	def __init__(self,position, speed, screen_height):
		super().__init__()
		self.image = pygame.Surface((4, 15)) # Image of the
		self.image.fill(COLOR_RED)
		self.rect = self.image.get_rect(center = position)
		self.speed = speed
		self.screen_height = screen_height

	def update(self):
		self.rect.y -= self.speed
		if self.rect.y > self.screen_height +15  or self.rect.y < 0:
			
			self.kill()