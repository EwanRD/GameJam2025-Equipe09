import pygame

from settings import PLAYER_HEALTH, PLAYER_COULDOWN, PLAYER_SPEED, PLAYER_DOMMAGE, DIRECTION, ARROW_DIRECTION
from .entity import Entity
import time

from src.projectiles.arrow import Arrow

class Player(Entity):
    def __init__(self, x, y, projectiles_group, walls):
        sprites = {
            "down": [
                pygame.image.load("assets/sprites/Player/devant.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/devantmarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/devantmarche2.png").convert_alpha(),
            ],
            "up": [
                pygame.image.load("assets/sprites/Player/derriere.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/derrieremarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/derrieremarche2.png").convert_alpha(),
            ],
            "left": [
                pygame.image.load("assets/sprites/Player/gauche.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/gauchemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/gauchemarche2.png").convert_alpha(),
            ],
            "right": [
                pygame.image.load("assets/sprites/Player/droite.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/droitemarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Player/droitemarche2.png").convert_alpha(),
            ],
        }
        super().__init__(x, y, sprites, PLAYER_SPEED)
        self.projectiles_group = projectiles_group
        self.last_shot_time = 0
        self.shoot_cooldown = PLAYER_COULDOWN
        self.health = PLAYER_HEALTH
        self.projectile_direction = DIRECTION.B.value
        self.projectile_sprite = ARROW_DIRECTION.B.value
        self.walls = walls

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # Mouvement horizontal
        if keys[pygame.K_LEFT]or keys[pygame.K_q]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]or keys[pygame.K_d]:
            dx = self.speed

        # Mouvement vertical
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        # Détermination direction projectile
        if dx < 0 and dy < 0:
            self.projectile_direction = DIRECTION.HG.value
            self.projectile_sprite = ARROW_DIRECTION.HG.value
        elif dx > 0 and dy < 0:
            self.projectile_direction = DIRECTION.HD.value
            self.projectile_sprite = ARROW_DIRECTION.HD.value
        elif dx < 0 and dy > 0:
            self.projectile_direction = DIRECTION.BG.value
            self.projectile_sprite = ARROW_DIRECTION.BG.value
        elif dx > 0 and dy > 0:
            self.projectile_direction = DIRECTION.BD.value
            self.projectile_sprite = ARROW_DIRECTION.BD.value
        elif dx < 0:
            self.projectile_direction = DIRECTION.G.value
            self.projectile_sprite = ARROW_DIRECTION.G.value
        elif dx > 0:
            self.projectile_direction = DIRECTION.D.value
            self.projectile_sprite = ARROW_DIRECTION.D.value
        elif dy < 0:
            self.projectile_direction = DIRECTION.H.value
            self.projectile_sprite = ARROW_DIRECTION.H.value
        elif dy > 0:
            self.projectile_direction = DIRECTION.B.value
            self.projectile_sprite = ARROW_DIRECTION.B.value

        # Tir
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = current_time

        # Déplacement
        self.move(dx, dy)

    def shoot(self):
        print(self.projectile_sprite)
        arrow = Arrow(self.rect.center, self.projectile_direction, PLAYER_DOMMAGE,self.projectile_sprite)
        shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.ogg")
        shoot_sound.set_volume(1)
        shoot_sound.play()
        self.projectiles_group.add(arrow) 

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            print("Player has died")
