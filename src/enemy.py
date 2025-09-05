import pygame
from .entity import Entity
import random
from .item import Item

class Ennemi(Entity):
    def __init__(self, x, y, sprites, walls, speed=3, all_sprites=None):
        super().__init__(x, y, sprites, speed)
        self.all_sprites = all_sprites
        self.walls = walls
        self.player = None  # Référence au joueur

    def set_player(self, player):
        """Définit la référence au joueur"""
        self.player = player

    def update(self, player_pos):
        """IA par défaut : suit le joueur seulement s'il n'est pas invisible"""
        # Si le joueur est invisible, ne pas le suivre
        if self.player and not self.player.invisibility.should_enemies_follow():
            return  # L'ennemi reste immobile

        dx, dy = 0, 0
        direction = self.direction
        directionHorizontale = abs(player_pos[0] - self.rect.x) > abs(player_pos[1] - self.rect.y)

        if player_pos[0] > self.rect.x:  # droite
            dx = self.speed
            if player_pos[1] < self.rect.y:  # haut
                dy = -self.speed
                if directionHorizontale:
                    direction = "right"
                else:
                    direction = "up"
            elif player_pos[1] > self.rect.y:  # bas
                dy = self.speed
                if directionHorizontale:
                    direction = "right"
                else:
                    direction = "down"
            else:  # alignée horizontalement
                direction = "right"
        elif player_pos[0] < self.rect.x:  # gauche
            dx = -self.speed
            if player_pos[1] < self.rect.y:  # haut
                dy = -self.speed
                if directionHorizontale:
                    direction = "left"
                else:
                    direction = "up"
            elif player_pos[1] > self.rect.y:  # bas
                dy = self.speed
                if directionHorizontale:
                    direction = "left"
                else:
                    direction = "down"
            else:  # alignée horizontalement
                direction = "left"
        else:  # alignee verticalement
            if player_pos[1] > self.rect.y:
                # bas
                dy = self.speed
                direction = "down"
            else:
                dy = -self.speed
                direction = "up"

        self.move(dx, dy, direction)

    def die(self):
        # Ajouter un kill au compteur du joueur
        if self.player:
            self.player.add_kill()
            print(f"Kills: {self.player.invisibility.kill_count}/10")
        self.kill()
        if self.all_sprites and random.random() < 0.3:  # 30% de chance de drop un item
            item_type = random.choice(["heart", "speed", "damage"])
            item = Item(self.rect.x, self.rect.y, item_type)
            self.all_sprites.add(item)