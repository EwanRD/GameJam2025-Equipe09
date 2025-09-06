import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites, speed=3):
        super().__init__()
        self.sprites = sprites
        print("Sprites keys:", sprites.keys())
        self.direction = "down"
        self.image = self.sprites[self.direction][0]
        # Réduire la hitbox de l'entity
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.inflate_ip(-25, -25)  # Réduit la hitbox de 8 pixels en largeur et hauteur

        # Animation
        self.speed = speed
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 10

        # Groupe de murs (assigné depuis l’extérieur ou une sous-classe)
        self.walls = None  

    def move(self, dx, dy, direction=None):
        moving = dx != 0 or dy != 0

        # Diagonale → vitesse réduite
        if dx != 0 and dy != 0:
            dx *= 0.7
            dy *= 0.7

        # --- Déplacement X ---
        self.rect.x += dx
        if self.walls:
            for mur in self.walls:
                if self.rect.colliderect(mur.rect):
                    if dx > 0:  # droite
                        self.rect.right = mur.rect.left
                    if dx < 0:  # gauche
                        self.rect.left = mur.rect.right

        # --- Déplacement Y ---
        self.rect.y += dy
        if self.walls:
            for mur in self.walls:
                if self.rect.colliderect(mur.rect):
                    if dy > 0:  # bas
                        self.rect.bottom = mur.rect.top
                    if dy < 0:  # haut
                        self.rect.top = mur.rect.bottom

        # --- Direction ---
        if direction:
            self.direction = direction
        else:
            if dx > 0: self.direction = "right"
            elif dx < 0: self.direction = "left"
            elif dy > 0: self.direction = "down"
            elif dy < 0: self.direction = "up"

        # --- Animation ---
        if moving:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % 3
            self.image = self.sprites[self.direction][self.anim_index]
        else:
            self.anim_index = 0
            self.image = self.sprites[self.direction][0]
