import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__()
        self.position = pygame.Vector2(position)  # position plus simple à manipuler
        self.velocity = pygame.Vector2(velocity)
        self.damage = damage

        # Valeurs par défaut, remplacées par les enfants (ex: Arrow)
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=position)

    def update(self, dt=1):
        """Met à jour la position du projectile."""
        self.position += self.velocity * dt
        self.rect.topleft = self.position
