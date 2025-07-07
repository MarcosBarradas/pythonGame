import pygame, sys

from code.Const import *

from code.SpaceShip import SpaceShip

class Game:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("VOADORES ESPACIAIS")
		self.clock = pygame.time.Clock()


	def run(self):
		spaceship = SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT)
		spaceship_group = pygame.sprite.GroupSingle()
		spaceship_group.add(spaceship)

		while True:
			# Checking for events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()


			# To Draw
			self.window.fill(COLOR_GREY)
			spaceship_group.draw(self.window)
			spaceship_group.sprite.lasers_group.draw(self.window)

			# To update
			spaceship_group.update()


			pygame.display.update()
			self.clock.tick(60)
