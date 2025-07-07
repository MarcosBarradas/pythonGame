import pygame, sys

from code.Const import *
from code.Obstacle import Obstacle
from code.SpaceShip import SpaceShip
from code.Obstacle import grid

class Game:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("VOADORES ESPACIAIS")
		self.clock = pygame.time.Clock()
		self.spaceship_group = pygame.sprite.GroupSingle()
		self.obstacles = self.create_obstacles()

	def run(self):
		# var
		spaceship = SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.spaceship_group.add(spaceship)

		while True:
			# Checking for events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()


			# To Draw
			self.window.fill(COLOR_GREY)
			self.spaceship_group.draw(self.window)
			self.spaceship_group.sprite.lasers_group.draw(self.window)
			for obstacle in self.obstacles: obstacle.blocks_group.draw(self.window)

			# To update
			self.spaceship_group.update()


			pygame.display.update()
			self.clock.tick(60)

	@staticmethod
	def create_obstacles():
		obstacle_width = len(grid[0]) * 3  # Calculate the length of the obstacle
		gap = (SCREEN_WIDTH - (4 * obstacle_width)) / 5  # Calculates the gap between obstacles
		obstacles = []

		for i in range(4):
			off_x = (i + 1) * gap + i * obstacle_width
			obstacle = Obstacle(off_x, SCREEN_HEIGHT - 200)
			obstacles.append(obstacle)

		return obstacles
