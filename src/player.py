import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.playerSprite = pygame.image.load("assets/sprites/Player/devant.png").convert_alpha()
        self.image.blit(self.playerSprite, (0, 0))
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