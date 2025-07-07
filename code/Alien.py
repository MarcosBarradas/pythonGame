import pygame

class Alien(pygame.sprite.Sprite):
	def __init__(self, type, x, y):
		super().__init__()
		self.type = type
		self.image = pygame.image.load(f"./assets/alien_{self.type}.png")
		self.rect = self.image.get_rect(topleft = (x, y))

	def update(self, direction):
		self.rect.x += direction

class MysteryShip(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("./assets/mystery_ship.png")
		self.rect = self.image.get_rect(topleft = (x, 40))