import pygame
from .enemy import Ennemi

class Ghost(Ennemi):
    def __init__(self, x, y, human):
        self.human = human
        self.health = 1

        sprites = {
            "down": [
                pygame.image.load("assets/sprites/Enemies/Ghost/devant.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/devantmarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/devantmarche2.png").convert_alpha(),
            ],
            "up": [
                pygame.image.load("assets/sprites/Enemies/Ghost/derriere.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/derrieremarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/derrieremarche2.png").convert_alpha(),
            ],            "left": [
                pygame.image.load("assets/sprites/Enemies/Ghost/gauche.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/gauchemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/gauchemarche2.png").convert_alpha(),
            ],
            "right": [
                pygame.image.load("assets/sprites/Enemies/Ghost/droite.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/droitemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Ghost/droitemarche2.png").convert_alpha(),
            ],
        }

        super().__init__(x, y, sprites, speed=4)

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            # death_sound = pygame.mixer.Sound("assets/sounds/orc_death.mp3")
            # death_sound.set_volume(1)
            # death_sound.play()
