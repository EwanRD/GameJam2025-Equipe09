import pygame
from src.projectiles.projectile import Projectile

class Fireball(Projectile):
    def __init__(self, position, velocity, damage):
        super().__init__(position, velocity, damage)
        self.image = pygame.image.load("assets/sprites/Projectiles/Ghost_burst/ghost_burst.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=position)

    def on_hit(self, target):
        target.take_damage()
        hit_sound = pygame.mixer.Sound("assets/sounds/hurt.mp3")
        hit_sound.set_volume(1)
        hit_sound.play()

    def update(self, dt=2):
        self.position += self.velocity * dt
        self.rect.topleft = self.position
