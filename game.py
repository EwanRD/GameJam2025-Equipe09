import pygame
import settings
import time
from src.player import Player
from src.skeleton import Skeleton

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
        self.heart_full = pygame.image.load("assets/sprites/UI/Heart/coeurplein.png").convert_alpha()
        self.heart_empty = pygame.image.load("assets/sprites/UI/Heart/coeurvide.png").convert_alpha()
        self.font = pygame.font.SysFont(None, 48)
        self.start_time = time.time()
        pygame.mixer.music.load("assets/sounds/crypt_loop.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)


        # Groupes
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # Joueur
        self.player = Player(100, 100, self.projectiles)
        self.all_sprites.add(self.player)
        self.skeleton = Skeleton(50, 50, self.player)
        self.all_sprites.add(self.skeleton)
    
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
        self.projectiles.update()

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        self.all_sprites.draw(self.screen)
        self.projectiles.draw(self.screen)

        # --- HUD ---
        # Affiche les cœurs (pleins pour les vies restantes, vides pour les vies perdues)
        total_lives = 3
        for i in range(total_lives):
            if i < self.player.health:
                self.screen.blit(self.heart_full, (0 + i * 70, 10))
            else:
                self.screen.blit(self.heart_empty, (0 + i * 70, 10))

        # Affiche le timer (compte à rebours 5 min)
        total_time = 300  # 5 minutes en secondes
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, total_time - elapsed)
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text = self.font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(timer_text, (settings.SCREEN_WIDTH / 2, 20))

        pygame.display.flip()
