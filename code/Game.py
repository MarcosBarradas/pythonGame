import pygame, sys

from code.Const import *
from code.SpaceShip import SpaceShip

class Game:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("VOADORES ESPACIAIS")
		self.clock = pygame.time.Clock()
		self.spaceShip = SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.spaceShip_group = pygame.sprite.GroupSingle()

	def run(self):
		self.spaceShip_group.add(self.spaceShip)
		while True:
			# Checking for events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()


			# To Draw
			self.window.fill(COLOR_GREY)
			self.spaceShip_group.draw(self.window)

			# To update
			self.spaceShip_group.update()

			pygame.display.update()
			self.clock.tick(60)
