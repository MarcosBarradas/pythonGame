import pygame, random

from code.Const import SCREEN_WIDTH, OFFSET


class Alien(pygame.sprite.Sprite):
	def __init__(self, type, x, y):
		super().__init__()
		self.type = type
		self.image = pygame.image.load(f"./assets/alien_{self.type}.png")
		self.rect = self.image.get_rect(topleft = (x, y))

	def update(self, direction):
		self.rect.x += direction

class MysteryShip(pygame.sprite.Sprite):
	def __init__(self, x):
		super().__init__()
		self.image = pygame.image.load("./assets/extra.png")

		x = random.choice([OFFSET / 2, SCREEN_WIDTH - self.image.get_width()])
		if x == 0:
			self.speed = 2
		else:
			self.speed = -2

		self.rect = self.image.get_rect(topleft = (x, 40))

	def update(self):
		self.rect.x += self.speed
		if self.rect.right > SCREEN_WIDTH or self.rect.left < 50:
			self.kill()
