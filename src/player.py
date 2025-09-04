import pygame
from .entity import Entity
import time

from src.projectiles.arrow import Arrow

class Player(Entity):
    def __init__(self, x, y, projectiles_group):
        sprites = {
            "down": [
                pygame.image.load("assets/sprites/Player/devant.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/devantmarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/devantmarche2.png").convert_alpha(),
            ],
            "up": [
                pygame.image.load("assets/sprites/Player/derriere.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/derrieremarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/derrieremarche2.png").convert_alpha(),
            ],
            "left": [
                pygame.image.load("assets/sprites/Player/gauche.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/gauchemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/gauchemarche2.png").convert_alpha(),
            ],
            "right": [
                pygame.image.load("assets/sprites/Player/droite.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/droitemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/droitemarche2.png").convert_alpha(),
            ],
        }
        super().__init__(x, y, sprites, speed=5)
        self.projectiles_group = projectiles_group
        self.last_shot_time = 0
        self.shoot_cooldown = 0.5

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            dx = -self.speed
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            dx = self.speed
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            dy = -self.speed
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            dy = self.speed
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = current_time
        self.move(dx, dy)

    def shoot(self):
        position = self.rect.center
        velocity = (8, 0)
        damage = 1
        arrow = Arrow(position, velocity, damage)
        self.projectiles_group.add(arrow)
