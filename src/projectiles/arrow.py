import pygame
import sprites
import settings
from src.utils import play_sound
from src.projectiles.projectile import Projectile

class Arrow(Projectile):
    def __init__(self, position, velocity, damage, sprite, shooter):
        super().__init__(position, velocity, damage)
        self.image = pygame.image.load(sprite).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.shooter = shooter
        
    def on_hit(self, target):
        # Utiliser les dégâts basés sur la difficulté
        base_damage = settings.get_current_player_stats()['damage']
        
        # Si le joueur a un boost de dégâts actif, utiliser les dégâts boostés
        if hasattr(self.shooter, "damage_boost_count") and self.shooter.damage_boost_count > 0:
            damage_to_deal = self.shooter.projectile_damage
            self.shooter.damage_boost_count -= 1
            
            if self.shooter.damage_boost_count == 0:
                self.shooter.projectile_damage = base_damage
        else:
            damage_to_deal = base_damage
            
        target.take_damage(damage_to_deal)
        play_sound(sprites.HIT_SOUND)

    def update(self, dt=2):
        self.position += self.velocity * dt
        self.rect.topleft = self.position