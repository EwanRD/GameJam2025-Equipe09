import pygame
from settings import ORC_HEALTH
import sprites
from .enemy import Ennemi


class Orc(Ennemi):
    def __init__(self, x, y, human, walls, all_sprites):
        self.human = human

        super().__init__(x, y, sprites.ORC_SPRITES, walls, speed=2, all_sprites=all_sprites)

        # Place health après super().__init__ pour éviter un overwrite
        self.health = ORC_HEALTH

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            # Jouer le son de mort avant la destruction
            death_sound = sprites.ORC_DEATH
            death_sound.set_volume(1)
            death_sound.play()

            self.die()
