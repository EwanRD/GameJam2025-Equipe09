import pygame
from src.projectiles.projectile import Projectile

class Arrow(Projectile):
    def __init__(self, position, velocity, damage):
        super().__init__(position, velocity, damage)
        self.image = pygame.image.load("assets/sprites/Arrow/flechedroite.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def on_hit(self, target):
        # Comportement spécifique si la flèche touche quelque chose
        pass
