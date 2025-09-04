import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites, speed=3):
        super().__init__()
        self.sprites = sprites
        self.direction = "down"
        self.image = self.sprites[self.direction][0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Animation
        self.speed = speed
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 10

    def move(self, dx, dy, direction=None):
        moving = dx != 0 or dy != 0

        # Diagonale → vitesse réduite
        if dx != 0 and dy != 0:
            dx *= 0.7
            dy *= 0.7

        self.rect.x += dx
        self.rect.y += dy

        # Déterminer la direction
        if direction:
            self.direction = direction
        else:
            if dx > 0: self.direction = "right"
            elif dx < 0: self.direction = "left"
            elif dy > 0: self.direction = "down"
            elif dy < 0: self.direction = "up"

        # Animation
        if moving:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % 3
            self.image = self.sprites[self.direction][self.anim_index]
        else:
            self.anim_index = 0
            self.image = self.sprites[self.direction][0]
