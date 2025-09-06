import pygame
import sprites
from src.projectiles.projectile import Projectile

class Arrow(Projectile):
    def __init__(self, position, velocity, damage,sprite, shooter):
        super().__init__(position, velocity, damage)
        self.image = pygame.image.load(sprite).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.shooter = shooter
    
    def on_hit(self, target):
        if hasattr(self.shooter, "projectile_damage"):
            target.take_damage(self.shooter.projectile_damage)
        else:
            target.take_damage(1)
        # TODO
        hit_sound = sprites.HIT_SOUND
        hit_sound.set_volume(1)
        hit_sound.play()
        if hasattr(self.shooter, "damage_boost_count") and self.shooter.damage_boost_count > 0:
            self.shooter.damage_boost_count -= 1
            if self.shooter.damage_boost_count == 0:
                self.shooter.projectile_damage = 1

    def update(self, dt=2):
        self.position += self.velocity * dt
        self.rect.topleft = self.position
