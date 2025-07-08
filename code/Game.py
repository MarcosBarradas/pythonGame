import pygame, sys, random

from code.Const import *
from code.Laser import Laser
from code.Obstacle import Obstacle
from code.SpaceShip import SpaceShip
from code.Obstacle import grid
from code.Alien import Alien, MysteryShip

class Game:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
		pygame.display.set_caption("VOADORES ESPACIAIS")
		self.clock = pygame.time.Clock()
		self.spaceship = SpaceShip()
		self.spaceship_group = pygame.sprite.GroupSingle()
		self.obstacles = self.create_obstacles()
		self.aliens = pygame.sprite.Group()
		self.create_aliens()
		self.alien_direction = 1
		self.alien_lasers_group = pygame.sprite.Group()
		self.mistery_ship_group = pygame.sprite.GroupSingle()
		self.lives = 3
		self.running = True


	def run(self):
		self.spaceship_group.add(self.spaceship)
		font = pygame.font.Font("./font/PixelifySans-Bold.ttf", 40)
		level_surface = font.render("LEVEL 01", False, COLOR_GREEN)
		game_over_surface = font.render("GAME OVER", False, COLOR_RED)
		pygame.time.set_timer(SHOOT_LASER, 300)
		pygame.time.set_timer(MYSTERYSHIP, random.randint(5050,9090))

		while True:
			# Checking for events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == SHOOT_LASER and self.running:
					self.alien_shoot_laser()

				if event.type == MYSTERYSHIP:
					self.create_mystery_ship()
					pygame.time.set_timer(MYSTERYSHIP, random.randint(5050,9090))

			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE] and self.running == False:
				self.reset()

			# To Draw
			self.window.fill(COLOR_GREY)
			self.window.blit(pygame.transform.scale(pygame.image.load("./assets/1.png").convert(),
			                                        (SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET)),
			                 (0, 0))
			pygame.draw.rect(self.window, COLOR_BLUE, (10,10,780,780), 2, 0, 60, 60, 60, 60)
			pygame.draw.line(self.window, COLOR_BLUE, (25,730), (755,730), 3)

			if self.running:
				self.window.blit(level_surface, (570,735,10,10))
			else:
				self.window.blit(game_over_surface, (550,735,10,10))

			for lie in range(self.lives):
				pass

			self.spaceship_group.draw(self.window)
			self.spaceship_group.sprite.lasers_group.draw(self.window)
			for obstacle in self.obstacles: obstacle.blocks_group.draw(self.window)
			self.aliens.draw(self.window)
			self.alien_lasers_group.draw(self.window)
			self.mistery_ship_group.draw(self.window)

			# To
			pygame.display.update()
			if self.running: # Condition stop the game if the live counter is 0
				self.spaceship_group.update()
				self.move_aliens()
				self.alien_lasers_group.update()
				self.mistery_ship_group.update()

				self.clock.tick(60)
				self.check_for_collisions()

	@staticmethod
	def create_obstacles():
		obstacle_width = len(grid[0]) * 3  # Calculate the length of the obstacle
		gap = (SCREEN_WIDTH + OFFSET - (4 * obstacle_width)) / 5  # Calculates the gap between obstacles
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
			elif alien.rect.left <= 50:
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

	def create_mystery_ship(self):
		self.mistery_ship_group.add(MysteryShip(SCREEN_WIDTH))

	# COLLISION
	def check_for_collisions(self):
		# Spaceship
		if self.spaceship_group.sprite.lasers_group:
			for laser_sprite in self.spaceship_group.sprite.lasers_group:
				if pygame.sprite.spritecollide(laser_sprite, self.aliens, True):
					laser_sprite.kill()
				if pygame.sprite.spritecollide(laser_sprite, self.mistery_ship_group, True):
					laser_sprite.kill()

				for obstacle in self.obstacles:
					if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
						laser_sprite.kill()

		# Alien Lasers
		if self.alien_lasers_group:
			for laser_sprite in self.alien_lasers_group:
				if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
					laser_sprite.kill()
					self.lives -= 1
					if self.lives == 0:
						self.gameover()

				for obstacle in self.obstacles:
					if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
						laser_sprite.kill()
		if self.aliens:
			for alien in self.aliens:
				for obstacle in self.obstacles:
					pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

				if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
					self.gameover()

	def gameover(self):
		self.running = False

	def reset(self):
		self.running = True
		self.lives = 3
		self.spaceship_group.sprite.reset()
		self.aliens.empty()
		self.alien_lasers_group.empty()
		self.mistery_ship_group.empty()
		self.obstacles = self.create_obstacles()
		self.create_aliens()
		self.alien_direction = 1
		self.spaceship.laser_ready = False
		self.spaceship.laser_time = 0
		self.spaceship.laser_delay = 300