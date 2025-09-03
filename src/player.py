import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.image.fill((0, 255, 0))  # carré vert temporaire
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] :
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] :
            self.rect.x += 5
        if keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_DOWN] :
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT] :
            self.rect.y += 5
        if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            self.rect.x -= 4
            self.rect.y += 4
        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            self.rect.x += 4
            self.rect.y += 4
        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            self.rect.x += 4
            self.rect.y -= 4
        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            self.rect.x -= 4
            self.rect.y -= 4