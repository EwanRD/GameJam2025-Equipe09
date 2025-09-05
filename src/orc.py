import pygame
from settings import ORC_HEALTH
from sprites import ORC_SPRITES, ORC_DEATH
from .enemy import Ennemi

class Orc(Ennemi):
    def __init__(self, x, y, human, walls, all_sprites):
        self.human = human
        self.health = ORC_HEALTH

        sprites = ORC_SPRITES

        super().__init__(x, y, sprites, walls, speed=2, all_sprites=all_sprites)

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            # TODO
            death_sound = ORC_DEATH
            death_sound.set_volume(1)
            death_sound.play()
            self.die()

