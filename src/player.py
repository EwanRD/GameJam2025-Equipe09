import pygame
import time

from src.projectiles.arrow import Arrow

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, projectiles_group):
        super().__init__()
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.playerSprite = pygame.image.load("assets/sprites/Player/devant.png").convert_alpha()
        self.image.blit(self.playerSprite, (0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.projectiles_group = projectiles_group
        self.last_shot_time = 0
        self.shoot_cooldown = 0.5


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] :
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] :
            self.rect.x += 5
        if keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] :
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] :
            self.rect.y += 5
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.rect.x -= 4
            self.rect.y += 4
        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.rect.x += 4
            self.rect.y += 4
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.rect.x += 4
            self.rect.y -= 4
        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.rect.x -= 4
            self.rect.y -= 4
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = current_time
        
    def shoot(self):
        position = self.rect.center
        velocity = (8, 0)
        damage = 1
        arrow = Arrow(position, velocity, damage)
        self.projectiles_group.add(arrow) 
