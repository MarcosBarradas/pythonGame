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
		self.player_ship = SpaceShip()
		self.player_group = pygame.sprite.GroupSingle()
		self.barriers = self.create_obstacles()
		self.invaders_group = pygame.sprite.Group()
		self.create_aliens()
		self.invader_direction = 1
		self.invader_shots = pygame.sprite.Group()
		self.ufo_group = pygame.sprite.GroupSingle()
		self.lives = 3
		self.running = True
		self.score = 0
		self.highscore = 0
		self.explosion_sound = pygame.mixer.Sound("./assets/explosion.mp3")
		pygame.mixer.music.load("./assets/music.mp3")
		pygame.mixer.music.play(-1)

	def run(self):
		self.player_group.add(self.player_ship)
		font = pygame.font.Font("./font/PixelifySans-Bold.ttf", 40)
		level_surface = font.render("LEVEL 01", False, COLOR_GREEN)
		game_over_surface = font.render("GAME OVER", False, COLOR_RED)
		score_text_surface = font.render("SCORE", False, COLOR_GREEN)
		highscore_text_surface = font.render("HIGHSCORE", False, COLOR_GREEN)
		pygame.time.set_timer(SHOOT_LASER, 300)
		pygame.time.set_timer(MYSTERYSHIP, random.randint(5050,9090))

		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == SHOOT_LASER and self.running:
					self.invader_shoot()
				if event.type == MYSTERYSHIP:
					self.spawn_ufo()
					pygame.time.set_timer(MYSTERYSHIP, random.randint(5050,9090))

			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE] and not self.running:
				self.reset()

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

			x = 50
			for life in range(self.lives):
				self.window.blit(self.player_group.sprite.image, (x, 735))
				x += 50

			self.window.blit(score_text_surface, (50,15,50,50))
			formatted_score = str(self.score).zfill(5)
			self.window.blit(font.render(formatted_score, False, COLOR_GREEN), (180,15,100,50))

			self.window.blit(highscore_text_surface, (550,15,50,50))
			formatted_high = str(self.highscore).zfill(5)
			self.window.blit(font.render(formatted_high, False, COLOR_GREEN), (630,50,100,50))

			self.player_group.draw(self.window)
			self.player_group.sprite.lasers_group.draw(self.window)
			for block in self.barriers:
				block.blocks_group.draw(self.window)
			self.invaders_group.draw(self.window)
			self.invader_shots.draw(self.window)
			self.ufo_group.draw(self.window)

			pygame.display.update()

			if self.running:
				self.player_group.update()
				self.move_invaders()
				self.invader_shots.update()
				self.ufo_group.update()
				self.clock.tick(60)
				self.check_for_collisions()

	@staticmethod
	def create_obstacles():
		obstacle_width = len(grid[0]) * 3
		gap = (SCREEN_WIDTH + OFFSET - (4 * obstacle_width)) / 5
		barriers = []
		for i in range(4):
			off_x = (i + 1) * gap + i * obstacle_width
			barriers.append(Obstacle(off_x, SCREEN_HEIGHT - 200))
		return barriers

	def create_aliens(self):
		for row in range(5):
			for col in range(11):
				alien_type = 3 if row == 0 else (2 if row in (1, 2) else 1)
				alien = Alien(alien_type, 75 + col * 55, 110 + row * 55)
				self.invaders_group.add(alien)

	def move_invaders(self):
		self.invaders_group.update(self.invader_direction)
		for alien in self.invaders_group.sprites():
			if alien.rect.right >= SCREEN_WIDTH:
				self.invader_direction = -1
				self.invader_move_down(2)
				break
			elif alien.rect.left <= 50:
				self.invader_direction = 1
				self.invader_move_down(2)
				break

	def invader_move_down(self, distance):
		for alien in self.invaders_group.sprites():
			alien.rect.y += distance

	def invader_shoot(self):
		if self.invaders_group.sprites():
			attacker = random.choice(self.invaders_group.sprites())
			laser = Laser(attacker.rect.center, -6, SCREEN_HEIGHT)
			self.invader_shots.add(laser)

	def spawn_ufo(self):
		self.ufo_group.add(MysteryShip(SCREEN_WIDTH))

	def check_for_collisions(self):
		# Player Lasers
		if self.player_group.sprite.lasers_group:
			for laser in self.player_group.sprite.lasers_group:
				hits = pygame.sprite.spritecollide(laser, self.invaders_group, True)
				if hits:
					for alien in hits:
						self.score += 10
						self.explosion_sound.play()
						laser.kill()
				if pygame.sprite.spritecollide(laser, self.ufo_group, True):
					self.score += 500
					self.explosion_sound.play()
					laser.kill()
				for block in self.barriers:
					if pygame.sprite.spritecollide(laser, block.blocks_group, True):
						laser.kill()

		# Invader Lasers
		for laser in self.invader_shots:
			if pygame.sprite.spritecollide(laser, self.player_group, False):
				laser.kill()
				self.lives -= 1
				if self.lives == 0:
					self.trigger_gameover()
			for block in self.barriers:
				if pygame.sprite.spritecollide(laser, block.blocks_group, True):
					laser.kill()

		# Invaders vs Player / Obstacles
		for alien in self.invaders_group:
			for block in self.barriers:
				pygame.sprite.spritecollide(alien, block.blocks_group, True)
			if pygame.sprite.spritecollide(alien, self.player_group, False):
				self.trigger_gameover()

	def trigger_gameover(self):
		self.update_highscore()
		self.running = False

	def reset(self):
		self.running = True
		self.lives = 3
		self.player_group.sprite.reset()
		self.invaders_group.empty()
		self.invader_shots.empty()
		self.ufo_group.empty()
		self.barriers = self.create_obstacles()
		self.score = 0
		self.create_aliens()
		self.invader_direction = 1
		self.player_ship.laser_ready = False
		self.player_ship.laser_time = 0
		self.player_ship.laser_delay = 300

	def update_highscore(self):
		if self.score > self.highscore:
			self.highscore = self.score
