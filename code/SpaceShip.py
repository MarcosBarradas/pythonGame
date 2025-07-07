import pygame
from code.Laser import Laser

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("./assets/player.png")
        self.rect = self.image.get_rect(midbottom = (self.screen_width / 2, self.screen_height - 100))
        self.speed = 5
        self.laser_ready = False
        self.laser_time = 0
        self.laser_delay = 300
        self.lasers_group = pygame.sprite.Group()

    def get_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height - 100)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks() # reset time

    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.lasers_group.update()
        self.recharge_laser()

    def constrain_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            # when time exceeds 300 ms
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True