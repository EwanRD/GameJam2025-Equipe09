import pygame
import media
from ..utils import play_sound
from src.projectiles.projectile import Projectile

class Fireball(Projectile):
    def __init__(self, position, velocity, damage):
        super().__init__(position, velocity, damage)
        self.image = media.FIREBALL_SPRITE
        self.rect = self.image.get_rect(topleft=position)
        play_sound(media.FIREBALL_SOUND)

    def on_hit(self, target):
        target.take_damage()
        play_sound(media.FIREBALL_HIT_SOUND)

    def update(self, dt=1):
        self.position += self.velocity * dt
        self.rect.topleft = self.position
