import pygame
import sprites
from settings import SKELETON_HEALTH
from .enemy import Ennemi


class Skeleton(Ennemi):
    def __init__(self, x, y, human, walls, all_sprites):
        self.human = human
        super().__init__(x, y, sprites.SKELETON_SPRITES, walls, speed=3, all_sprites=all_sprites)
        self.health = SKELETON_HEALTH

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self, amount=1):
        """Réduit la vie du squelette et gère sa mort"""
        self.health -= amount        
        if self.health <= 0:
            sprites.DEATH_SOUND.set_volume(1)
            sprites.DEATH_SOUND.play()
            self.die()
