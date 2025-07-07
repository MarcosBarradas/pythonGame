import pygame, sys, random

from code.Const import *
from code.Laser import Laser
from code.Obstacle import Obstacle
from code.SpaceShip import SpaceShip
from code.Obstacle import grid
from code.Alien import Alien

class Game:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("VOADORES ESPACIAIS")
		self.clock = pygame.time.Clock()
		self.spaceship = SpaceShip(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.spaceship_group = pygame.sprite.GroupSingle()
		self.obstacles = self.create_obstacles()
		self.aliens = pygame.sprite.Group()
		self.create_aliens()
		self.alien_direction = 1
		self.alien_lasers_group = pygame.sprite.Group()


	def run(self):
		# var

		self.spaceship_group.add(self.spaceship)
		pygame.time.set_timer(SHOOT_LASER, 300)

		while True:
			# Checking for events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == SHOOT_LASER:
					self.alien_shoot_laser()


			# To Draw
			self.window.fill(COLOR_GREY)
			self.spaceship_group.draw(self.window)
			self.spaceship_group.sprite.lasers_group.draw(self.window)
			for obstacle in self.obstacles: obstacle.blocks_group.draw(self.window)
			self.aliens.draw(self.window)
			self.alien_lasers_group.draw(self.window)

			# To update
			self.spaceship_group.update()
			self.move_aliens()
			self.alien_lasers_group.update()

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


	def create_aliens(self):
		for i in range(5):
			for j in range(11):
				alien_type = 3 if i == 0 else (2 if i in (1, 2) else 1)
				alien = Alien(alien_type, 75 + j * 55, 110 + i * 55)
				self.aliens.add(alien)

	def move_aliens(self):
		self.aliens.update(self.alien_direction)
		alien_sprites = self.aliens.sprites()
		for alien in alien_sprites:
			if alien.rect.right >= SCREEN_WIDTH:
				self.alien_direction = -1
				self.alien_move_down(2)
				break
			elif alien.rect.left <= 0:
				self.alien_direction = 1
				self.alien_move_down(2)
				break


	def alien_move_down(self, distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance

	def alien_shoot_laser(self):
		if self.aliens.sprites():
			random_alien = random.choice(self.aliens.sprites()) # it selects a random alien
			laser_sprite = Laser(random_alien.rect.center,-6, SCREEN_HEIGHT)
			self.alien_lasers_group.add(laser_sprite)