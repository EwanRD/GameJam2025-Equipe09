import pygame

from settings import PLAYER_DOMMAGE, PLAYER_COULDOWN, PROJ_SPEED
from .enemy import Ennemi
import math
import time

from .projectiles.fireball import Fireball


class Ghost(Ennemi):
    def __init__(self, x, y, human, projectiles, walls, all_sprites):
        self.human = human
        self.health = 1
        self.projectiles_group = projectiles
        self.last_shot_time = 0
        self.shoot_cooldown = PLAYER_COULDOWN
        self.projectiles_direction = 0,0
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

        super().__init__(x, y, sprites, walls, speed=4, all_sprites=all_sprites)

    def get_direction_vector(self, src_x, src_y, dst_x, dst_y, speed=PROJ_SPEED):
        dx = dst_x - src_x
        dy = dst_y - src_y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return 0, 0
        return speed * dx / distance, speed * dy / distance

    def update(self):

        self.projectiles_direction = self.get_direction_vector(self.rect.x, self.rect.y, self.human.rect.x,self.human.rect.y )
        """Suit directement le joueur associé"""
        if abs(self.human.rect.x - self.rect.x) > 600 or abs(self.human.rect.y - self.rect.y) > 450 :
            player_pos = (self.human.rect.x, self.human.rect.y)
            super().update(player_pos)
        else :
            current_time = time.time()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        fireball = Fireball(self.rect.center, self.projectiles_direction, PLAYER_DOMMAGE)
        shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.ogg")
        shoot_sound.set_volume(1)
        shoot_sound.play()
        self.projectiles_group.add(fireball)

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            # death_sound = pygame.mixer.Sound("assets/sounds/orc_death.mp3")
            # death_sound.set_volume(1)
            # death_sound.play()
            self.die()
