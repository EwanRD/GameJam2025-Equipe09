import pygame
import settings
from src.player import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("TOMB BOUND")
        self.clock = pygame.time.Clock()
        self.running = True
        self.bg_image = pygame.transform.scale(
            pygame.image.load("assets/mapgamejam.png").convert(),
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(100, 100)
        self.all_sprites.add(self.player)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
