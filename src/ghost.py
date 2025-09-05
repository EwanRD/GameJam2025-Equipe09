import pygame
from sprites import GHOST_SPRITES
from settings import GHOST_HEALTH
from .enemy import Ennemi

class Ghost(Ennemi):
    def __init__(self, x, y, human, walls, all_sprites):
        self.human = human
        self.health = GHOST_HEALTH

        sprites = GHOST_SPRITES
        super().__init__(x, y, sprites, walls, speed=4, all_sprites=all_sprites)

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            # TODO
            # death_sound = pygame.mixer.Sound("assets/sounds/orc_death.mp3")
            # death_sound.set_volume(1)
            # death_sound.play()
            self.die()
