import pygame
from .enemy import Ennemi

class Skeleton(Ennemi):
    def __init__(self, x, y, human):
        self.human = human
        self.health = 2

        sprites = {
            "down": [
                pygame.image.load("assets/sprites/Enemies/Squelette/devant.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/devantmarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/devantmarche2.png").convert_alpha(),
            ],
            "up": [
                pygame.image.load("assets/sprites/Enemies/Squelette/derriere.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/derrieremarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/derrieremarche2.png").convert_alpha(),
            ],            "left": [
                pygame.image.load("assets/sprites/Enemies/Squelette/gauche.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/gauchemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/gauchemarche2.png").convert_alpha(),
            ],
            "right": [
                pygame.image.load("assets/sprites/Enemies/Squelette/droite.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/droitemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/droitemarche2.png").convert_alpha(),
            ],
        }

        super().__init__(x, y, sprites, speed=3)

    def update(self):
        """Suit directement le joueur associé"""
        player_pos = (self.human.rect.x, self.human.rect.y)
        super().update(player_pos)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            death_sound = pygame.mixer.Sound("assets/sounds/skeleton_death.mp3")
            death_sound.set_volume(1)
            death_sound.play()
