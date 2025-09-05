import pygame
import random
import settings
import time
from src.player import Player
from src.enemy import Ennemi
from src.skeleton import Skeleton
from src.item import Item
from src.walls import Wall
from src.orc import Orc
from src.ghost import Ghost

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
        self.spawn_zones = [(682, 15), (1242, 420), (562, 855), (6, 419)]

        # --- Groupes ---
        self.all_sprites = pygame.sprite.Group()
        self.wall_list_player = pygame.sprite.Group()
        self.wall_list_enemy = pygame.sprite.Group()  # Liste de murs différente pour les ennemis
        self.projectiles = pygame.sprite.Group()

        # --- Joueur ---
        self.player = Player(625, 410, self.projectiles, self.wall_list_player)
        self.all_sprites.add(self.player)

        # --- Initialisation des vagues ---
        self.wave = 1
        self.wave_start_time = time.time()
        self.wave_interval = 10  # secondes entre chaque vague
        self.wave_enemy_count = 3
        self.wave_types = [Skeleton, Orc, Ghost]  # tous types d'ennemis dès le début

        # Spawn initial après avoir créé le joueur et les groupes
        self.spawn_enemies(self.wave_enemy_count)

        # --- Musique ---
        pygame.mixer.music.load("assets/sounds/crypt_loop.wav")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Murs
        # Mur à gauche : Haut
        wall = Wall(0,0,30,299)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)
        # Ouverture à gauche
        wall = Wall(0,299,10,300)
        self.wall_list_player.add(wall)
        # Mur à gauche : Bas
        wall = Wall(0,599,30,settings.SCREEN_HEIGHT-30)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)

        # Mur du haut : Gauche
        wall = Wall(0,0,568,85)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)
        # Ouverture du haut
        wall = Wall(568,0,286,10)
        self.wall_list_player.add(wall)
        # Mur du haut : Droite
        wall = Wall(854,0,settings.SCREEN_WIDTH,85)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)

        # Mur à droite : Haut
        wall = Wall (settings.SCREEN_WIDTH-55,0,55,299)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)
        # Ouverture à droite
        wall = Wall (settings.SCREEN_WIDTH-35,299,35,300)
        self.wall_list_player.add(wall)
        # Mur à droite : Bas
        wall = Wall (settings.SCREEN_WIDTH-55,599,55,settings.SCREEN_HEIGHT)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)

        # Mur du bas : Gauche
        wall = Wall (0,settings.SCREEN_HEIGHT-60,426,60)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)
        # Ouverture du bas
        wall = Wall (426,settings.SCREEN_HEIGHT-40,286,40)
        self.wall_list_player.add(wall)
        # Mur du bas : Droite
        wall = Wall (712,settings.SCREEN_HEIGHT-60,settings.SCREEN_WIDTH,60)
        self.wall_list_player.add(wall)
        self.wall_list_enemy.add(wall)




    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.all_sprites.update()
        self.projectiles.update()
        self.wall_list_player.update()

        # --- Enemy spawn logic (non-blocking) ---
        if hasattr(self, 'enemies_to_spawn') and self.enemies_to_spawn > 0:
            if time.time() >= self.next_spawn_time:
                spawn_x, spawn_y = random.choice(self.spawn_zones)
                enemy_type = random.choice(self.current_wave_types)
                enemy = enemy_type(spawn_x, spawn_y, self.player, self.wall_list_enemy, self.all_sprites)
                enemy.set_player(self.player)  # Associer le joueur à l'ennemi
                self.all_sprites.add(enemy)
                self.enemies_to_spawn -= 1
                self.next_spawn_time = time.time() + self.spawn_cooldown

        # --- Projectiles hit enemies ---
        for projectile in self.projectiles:
            for enemy in self.all_sprites:
                if enemy != self.player and isinstance(enemy, Ennemi) and projectile.rect.colliderect(enemy.rect):
                    projectile.on_hit(enemy)
                    projectile.kill()

        # --- Player collision with enemies ---
        for enemy in self.all_sprites:
            if enemy != self.player and not isinstance(enemy, Item) and not self.player.is_invincible() and self.player.rect.colliderect(enemy.rect):
                self.player.take_damage()
                dx = enemy.rect.x - self.player.rect.x
                dy = enemy.rect.y - self.player.rect.y
                distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                knockback_strength = 80
                knockback_x = int(knockback_strength * dx / distance)
                knockback_y = int(knockback_strength * dy / distance)
                enemy.move(knockback_x, knockback_y)
                hurt_sound = pygame.mixer.Sound("assets/sounds/hurt.mp3")
                hurt_sound.set_volume(1)
                hurt_sound.play()
                if self.player.health <= 0:
                    pygame.mixer.music.stop()
                    game_over_sound = pygame.mixer.Sound("assets/sounds/GameOver.wav")
                    game_over_sound.set_volume(1)
                    game_over_sound.play()
                    pygame.time.delay(5000)
                    self.__init__()
                    self.run()

        # Collisions avec les items
        for sprite in self.all_sprites:
            if isinstance(sprite, Item) and self.player.rect.colliderect(sprite.rect):
                sprite.apply_effect(self.player)
                sprite.kill()

        # --- Gestion des vagues ---
        enemies_alive = any(isinstance(s, (Skeleton, Orc, Ghost)) for s in self.all_sprites)
        total_time = 300
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, total_time - elapsed)

        if remaining > 0:
            if not enemies_alive and (not hasattr(self, 'enemies_to_spawn') or self.enemies_to_spawn == 0):
                self.wave_start_time = time.time()
                # Définir les types et nombres selon la vague
                if self.wave == 1:
                    self.wave_enemy_count = 3            
                    self.player.add_kill()
                    self.current_wave_types = [Skeleton]
                elif self.wave == 2:
                    self.wave_enemy_count = 5
                    self.current_wave_types = [Skeleton, Orc]
                else:
                    self.wave_enemy_count = 8
                    self.current_wave_types = [Skeleton, Orc, Ghost]

                self.spawn_enemies(self.wave_enemy_count)
                self.wave += 1  # passe à la vague suivante

    def run(self):
        while self.running:
            events = pygame.event.get()
            self.handle_events(events)
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        # Dessiner tous les sprites avec gestion de l'invisibilité et du clignotement
        for sprite in self.all_sprites:
            if not isinstance(sprite, Item):
                # Si c'est le joueur
                if sprite == self.player:
                    # Clignotement pendant l'invincibilité après dégâts
                    if self.player.invincible_after_damage and not self.player.visible:
                        continue
                    # Invisibilité du pouvoir
                    elif self.player.invisibility.invisible:
                        temp_surface = sprite.image.copy()
                        temp_surface.set_alpha(128)  # 50% de transparence
                        self.screen.blit(temp_surface, sprite.rect)
                    else:
                        self.screen.blit(sprite.image, sprite.rect)
                else:
                    self.screen.blit(sprite.image, sprite.rect)

        # Dessiner les items visibles
        for sprite in self.all_sprites:
            if isinstance(sprite, Item) and hasattr(sprite, "visible") and sprite.visible:
                self.screen.blit(sprite.image, sprite.rect)

        self.projectiles.draw(self.screen)

        # --- HUD ---
        total_lives = 3
        for i in range(total_lives):
            if i < self.player.health:
                self.screen.blit(self.heart_full, (0 + i * 70, 10))
            else:
                self.screen.blit(self.heart_empty, (0 + i * 70, 10))

        total_time = 300
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, total_time - elapsed)
        minutes = remaining // 60
        seconds = remaining % 60
        timer_text = self.font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(timer_text, (settings.SCREEN_WIDTH // 2, 20))

        self.player.invisibility.draw_power_bar(self.screen, 10, 100)

        player_pos = self.player.rect.center
        pos_text = self.font.render(f"X: {player_pos[0]}  Y: {player_pos[1]}", True, (255, 255, 0))
        self.screen.blit(pos_text, (20, settings.SCREEN_HEIGHT - 60))


        pygame.display.flip()

    def spawn_enemies(self, count, cooldown=0.3):
        self.spawned = 0
        self.next_spawn_time = time.time()
        self.enemies_to_spawn = count
        self.spawn_cooldown = cooldown

        # Définir les types d'ennemis selon la vague
        if self.wave == 1:
            self.current_wave_types = [Skeleton]
        elif self.wave == 2:
            self.current_wave_types = [Skeleton, Orc]
        else:  # vague 3 et suivantes
            self.current_wave_types = [Skeleton, Orc, Ghost]

    def reset(self):
        self.__init__()
