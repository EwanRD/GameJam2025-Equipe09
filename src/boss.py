import pygame
import time
import random
import sprites
from .utils import play_sound
from .entity import Entity


class Boss(Entity):
    def __init__(self, x, y, human):
        self.human = human
        self.health = 2

        self.sprites = sprites.BOSS_SPRITES

        super().__init__(x, y, sprites, speed=0)
        self.spawn_time = time.time()
        self.state = "spawning"
        self.last_teleport = time.time()
        self.corners = [
            (0, 0),
            (1280 - self.rect.width, 0), 
            (0, 900 - self.rect.height),
            (800 - self.rect.width, 600 - self.rect.height)
        ]
    
    def update(self):
        now = time.time()
        if self.state == "spawning":
            if now - self.spawn_time > 5:
                self.state = "teleport"
                self.teleport()
                self.last_teleport = now
        elif self.state == "teleport":
            self.shoot_at_player()
            self.state = "waiting"
            self.last_teleport = now
        elif self.state == "waiting":
            if now - self.last_teleport > 1:
                self.state = "teleport"
                self.teleport()


    def teleport(self):
        self.x, self.y = random.choice(self.corners)
        self.rect.topleft = (self.x, self.y)

    def shoot_at_player(self):
        # Ajoute ici la logique pour tirer sur le joueur (human)
        pass

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            play_sound(sprites.DEATH_SOUND)
