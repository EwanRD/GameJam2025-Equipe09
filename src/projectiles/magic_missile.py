import pygame
import sprites
from ..utils import play_sound
from src.projectiles.projectile import Projectile

class Magic_Missile(Projectile):
    def __init__(self, position, velocity, damage):
        super().__init__(position, velocity, damage)
        self.image = sprites.FIREBALL_SPRITE
        self.rect = self.image.get_rect(topleft=position)
        play_sound(sprites.FIREBALL_SOUND)

    def on_hit(self, target):
        target.take_damage()
        play_sound(sprites.FIREBALL_HIT_SOUND)

    def update(self, dt=1):
        self.position += self.velocity * dt
        self.rect.topleft = self.position