import pygame
from .entity import Entity

class Ennemi(Entity):
    def __init__(self, x, y, sprites, walls, speed=3):
        super().__init__(x, y, sprites, speed)
        self.walls = walls

    def update(self, player_pos):
        """IA par défaut : suit le joueur"""
        dx, dy = 0, 0
        direction = self.direction  # garder la dernière direction par défaut
        directionHorizontale = abs(player_pos[0] - self.rect.x )> abs(player_pos[1] - self.rect.y)

        if player_pos[0] > self.rect.x : # droite
            dx = self.speed
            if player_pos[1] < self.rect.y : # haut
                dy = -self.speed
                if directionHorizontale :
                    direction = "right"
                else :
                    direction = "up"
            elif player_pos[1] > self.rect.y  : # bas
                dy = self.speed
                if directionHorizontale :
                    direction = "right"
                else :
                    direction = "down"
            else : # alignée horizontalement
                direction = "right"
        elif player_pos[0] < self.rect.x : # gauche
            dx = -self.speed
            if player_pos[1] < self.rect.y : # haut
                dy = -self.speed
                if directionHorizontale :
                    direction = "left"
                else :
                    direction = "up"
            elif player_pos[1] > self.rect.y  : # bas
                dy = self.speed
                if directionHorizontale :
                    direction = "left"
                else :
                    direction = "down"
            else : # alignée horizontalement
                direction = "left"
        else : # alignee verticalement
            if player_pos[1] > self.rect.y  :
                # bas
                dy = self.speed
                direction = "down"
            else :
                dy = -self.speed
                direction = "up"

        self.move(dx, dy, direction)
