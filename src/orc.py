import pygame
from .enemy import Ennemi

class Orc(Ennemi):
    def __init__(self, x, y, human):
        self.human = human
        self.health = 3

        sprites = {
            "down": [
                pygame.image.load("assets/sprites/Enemies/Orc/devant.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/devantmarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/devantmarche2.png").convert_alpha(),
            ],
            "up": [
                pygame.image.load("assets/sprites/Enemies/Orc/derriere.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/derrieremarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/derrieremarche2.png").convert_alpha(),
            ],            "left": [
                pygame.image.load("assets/sprites/Enemies/Orc/gauche.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/gauchemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/gauchemarche2.png").convert_alpha(),
            ],
            "right": [
                pygame.image.load("assets/sprites/Enemies/Orc/droite.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/droitemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Orc/droitemarche2.png").convert_alpha(),
            ],
        }

        super().__init__(x, y, sprites, speed=2.5)

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            death_sound = pygame.mixer.Sound("assets/sounds/orc_death.mp3")
            death_sound.set_volume(1)
            death_sound.play()
