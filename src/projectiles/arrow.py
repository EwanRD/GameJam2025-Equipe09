import pygame
from src.projectiles.projectile import Projectile

class Arrow(Projectile):
    def __init__(self, position, velocity, damage,sprite):
        super().__init__(position, velocity, damage)
        self.image = pygame.image.load(sprite).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def on_hit(self, target):
        target.take_damage()