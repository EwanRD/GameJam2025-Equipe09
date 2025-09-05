import pygame
from sprites import SKELETON_SPRITES, DEATH_SOUND
from settings import SKELETON_HEALTH
from .enemy import Ennemi


class Skeleton(Ennemi):
    def __init__(self, x, y, human, walls, all_sprites):
        self.human = human
        self.health = SKELETON_HEALTH

        sprites = SKELETON_SPRITES

        super().__init__(x, y, sprites, walls, speed=3, all_sprites=all_sprites)

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self, amount=1):
        self.health -= amount        
        if self.health <= 0:
            # TODO
            death_sound = DEATH_SOUND
            death_sound.set_volume(1)
            death_sound.play()
            self.die()
