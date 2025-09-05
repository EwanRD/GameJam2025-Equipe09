import pygame
import time

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        if item_type == "heart":
            self.image = pygame.image.load("assets/sprites/item/coeurplein.png").convert_alpha()
        elif item_type == "speed":
            self.image = pygame.image.load("assets/sprites/item/boots.png").convert_alpha()
        elif item_type == "damage":
            self.image = pygame.image.load("assets/sprites/item/flechehautdroite.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_time = time.time()
        self.visible = True

    def update(self):
        elapsed = time.time() - self.spawn_time
        if elapsed > 7:
            self.visible = int(elapsed * 5) % 2 == 0
        else:
            self.visible = True
        if elapsed > 10:
            self.kill()

    def apply_effect(self, player):
        if self.item_type == "heart":
            player.health = min(player.health + 1, 3)
        elif self.item_type == "speed":
            player.speed += 2
            player.speed_boost_end = time.time() + 5
        elif self.item_type == "damage":
            if player.projectile_damage < 3:
                player.projectile_damage = 3
            if player.damage_boost_count <= 0:
                player.damage_boost_count = 3