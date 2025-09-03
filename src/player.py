import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))  # carré vert temporaire
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]and not keys[pygame.K_DOWN] or keys[pygame.K_LEFT] and not keys[pygame.K_UP]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN] or keys[pygame.K_RIGHT] and not keys[pygame.K_UP]:
            self.rect.x += 5
        if keys[pygame.K_UP] and not keys[pygame.K_LEFT] or keys[pygame.K_UP] and not keys[pygame.K_RIGHT]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] or keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT]:
            self.rect.y += 5
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.rect.x -= 2
            self.rect.y += 2