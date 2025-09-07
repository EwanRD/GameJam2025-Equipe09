import pygame
import random
import settings
import sprites 
import time
from src.utils import play_sound
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
        # Charger tous les sprites maintenant que la fenêtre est prête
        sprites.load_sprites()
        self.clock = pygame.time.Clock()
        self.running = True
        self.bg_image = pygame.transform.scale(sprites.MAP,
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )
        self.heart_full = sprites.HEART_FULL
        self.heart_empty =sprites.HEART_EMPTY
        self.font = pygame.font.SysFont(None, 48)
        self.start_time = time.time()
        self.spawn_zones = settings.SPAWN_ZONE
        
        # Utiliser le temps total basé sur la difficulté
        self.total_time = settings.get_current_total_time()
        
        pygame.mixer.music.load(sprites.BACKGROUND_MUSIC)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)


        # --- Groupes ---
        self.all_sprites = pygame.sprite.Group()
        self.wall_list_player = pygame.sprite.Group()
        self.wall_list_enemy = pygame.sprite.Group() # Liste de murs différente pour les ennemis qui rentre par les ouvertures
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()

        # --- Joueur ---
        self.player = Player(625, 410, self.player_projectiles, self.wall_list_player)
        self.all_sprites.add(self.player)

        # --- Initialisation des vagues ---
        self.wave = 1
        self.wave_start_time = time.time()
        self.wave_interval = 10  # secondes entre chaque vague
        self.wave_enemy_count = 3
        self.wave_types = [Skeleton]  # tous types d'ennemis dès le début

        # Spawn initial après avoir créé le joueur et les groupes
        self.spawn_enemies(self.wave_enemy_count)

        # --- Musique ---
        pygame.mixer.music.load(sprites.BACKGROUND_MUSIC)
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

        self.wave = settings.FIRST_WAVE
        self.wave_start_time = time.time()
        self.wave_interval = settings.WAVE_INTERVAL  # secondes entre chaque vague
        self.wave_enemy_count = settings.ENEMY_COUNT
        self.wave_types = [Skeleton]  # types d'ennemis pour la première vague

    def run(self):
        while self.running:
            self.handle_events()
            
            # Vérifier si le temps est écoulé
            elapsed = int(time.time() - self.start_time)
            if elapsed >= self.total_time:
                # Le joueur a survécu au temps imparti - victoire !
                pygame.mixer.music.stop()
                # Vous pouvez ajouter ici un son de victoire ou retourner un état de victoire
                return "victory"
            
            result = self.update()
            if result == "game_over":
                return result
                
            self.draw()
            self.clock.tick(settings.FPS)
            
            # Gestion des vagues
            # Démarre la première vague au lancement du jeu
            if self.wave == 1 and not hasattr(self, 'enemies_to_spawn'):
                self.spawn_enemies(self.wave_enemy_count)
            elif time.time() - self.wave_start_time > self.wave_interval:
                self.wave += 1
                if self.wave_interval < 20: 
                    self.wave_interval += 5
                self.wave_start_time = time.time()
                # Augmente le nombre d'ennemis à chaque vague
                if self.wave_enemy_count < settings.ENEMY_COUNT:
                    self.wave_enemy_count += self.wave
                # Ajoute des types d'ennemis au fil des vagues
                if self.wave == 2 and Orc not in self.wave_types:
                    self.wave_types.append(Orc)
                if self.wave == 3 and Ghost not in self.wave_types:
                    self.wave_types.append(Ghost)
                self.spawn_enemies(self.wave_enemy_count)

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.all_sprites.update()
        self.player_projectiles.update()
        self.enemy_projectiles.update()
        self.wall_list_player.update()

        # --- Enemy spawn logic (non-blocking) ---
        if hasattr(self, 'enemies_to_spawn') and self.enemies_to_spawn > 0:
            if time.time() >= self.next_spawn_time:
                spawn_x, spawn_y = random.choice(self.spawn_zones)
                enemy_type = random.choice(self.wave_types)
                if enemy_type == Ghost :
                    enemy = enemy_type(spawn_x, spawn_y, self.player, self.enemy_projectiles, self.wall_list_enemy, self.all_sprites)
                else :
                    enemy = enemy_type(spawn_x, spawn_y, self.player, self.wall_list_enemy, self.all_sprites)
                # IMPORTANT: Donner la référence du joueur à l'ennemi
                enemy.set_player(self.player)
                self.all_sprites.add(enemy)
                self.enemies_to_spawn -= 1
                self.next_spawn_time = time.time() + self.spawn_cooldown

        # Collisions projectiles-ennemis
        for projectile in self.player_projectiles:

            for enemy in self.all_sprites:
                if enemy != self.player and isinstance(enemy, Ennemi) and projectile.rect.colliderect(enemy.rect):
                    projectile.on_hit(enemy)
                    projectile.kill()

        for projectile in self.enemy_projectiles:
            for player in self.all_sprites:
                if isinstance(player, Player) and projectile.rect.colliderect(player.rect):
                    projectile.on_hit(player)
                    projectile.kill()

        if self.player.invisibility.can_take_damage():
            for enemy in self.all_sprites:
                if enemy != self.player and isinstance(enemy, Ennemi) and self.player.rect.colliderect(enemy.rect):
                    self.player.take_damage()
                    dx = enemy.rect.x - self.player.rect.x
                    dy = enemy.rect.y - self.player.rect.y
                    distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                    knockback_strength = 80
                    knockback_x = int(knockback_strength * dx / distance)
                    knockback_y = int(knockback_strength * dy / distance)
                    enemy.move(knockback_x, knockback_y)
                    play_sound(sprites.HURT_SOUND)
                    if self.player.health <= 0:
                        pygame.mixer.music.stop()
                        play_sound(sprites.GAMEOVER_SOUND)
                        return "game_over"

        # --- Player collision with enemies ---
        for enemy in self.all_sprites:
            if enemy != self.player and not isinstance(enemy, Item) and self.player.rect.colliderect(enemy.rect):
                self.player.take_damage()
                dx = enemy.rect.x - self.player.rect.x
                dy = enemy.rect.y - self.player.rect.y
                distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                knockback_strength = 80
                knockback_x = int(knockback_strength * dx / distance)
                knockback_y = int(knockback_strength * dy / distance)
                enemy.move(knockback_x, knockback_y)
                play_sound(sprites.HURT_SOUND)
                if self.player.health <= 0:
                    pygame.mixer.music.stop()
                    return "game_over"

        # Collisions avec les items
        for sprite in self.all_sprites:
            if isinstance(sprite, Item) and self.player.rect.colliderect(sprite.rect):
                sprite.apply_effect(self.player)
                sprite.kill()

        # --- Gestion des vagues ---
        enemies_alive = any(isinstance(s, (Skeleton, Orc, Ghost)) for s in self.all_sprites)
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, self.total_time - elapsed)

        if remaining > 0:
            if not enemies_alive and (not hasattr(self, 'enemies_to_spawn') or self.enemies_to_spawn == 0):
                self.wave_start_time = time.time()
                # Définir les types et nombres selon la vague
                if self.wave == 1:
                    self.wave_enemy_count = 3
                    self.player.add_kill()
                    self.wave_types = [Skeleton]
                elif self.wave == 2:
                    self.wave_enemy_count = 5
                    self.wave_types = [Skeleton, Orc]
                else:
                    self.wave_enemy_count = 8
                    self.wave_types = [Skeleton, Orc, Ghost]

                self.spawn_enemies(self.wave_enemy_count)
                self.wave += 1  # passe à la vague suivante

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        
        self.player_projectiles.draw(self.screen)
        self.enemy_projectiles.draw(self.screen)

        # Dessiner tous les sprites avec gestion de l'invisibilité et du clignotement
        for sprite in self.all_sprites:
            if not isinstance(sprite, Item):
                # Si c'est le joueur
                if sprite == self.player:
                    # Clignotement pendant l'invincibilité après dégâts
                    if self.player.invincible_after_damage:
                        if self.player.visible:
                            self.screen.blit(sprite.image, sprite.rect)
                    # Invisibilité du pouvoir (transparence)
                    elif self.player.invisibility.invisible:
                        temp_surface = sprite.image.copy()
                        temp_surface.set_alpha(128)  # 50% de transparence
                        self.screen.blit(temp_surface, sprite.rect)
                    # Affichage normal
                    else:
                        self.screen.blit(sprite.image, sprite.rect)
                else:
                    # Affichage normal pour tous les autres sprites (ennemis, etc.)
                    self.screen.blit(sprite.image, sprite.rect)

        # Dessiner les items avec leur logique de clignotement
        for sprite in self.all_sprites:
            if isinstance(sprite, Item):
                if hasattr(sprite, "visible") and sprite.visible:
                    self.screen.blit(sprite.image, sprite.rect)
                elif not hasattr(sprite, "visible"):
                    # Items sans logique de clignotement (affichage normal)
                    self.screen.blit(sprite.image, sprite.rect)

        # --- HUD ---
        max_hearts = self.player.max_health
        for i in range(max_hearts):
            if i < self.player.health:
                self.screen.blit(self.heart_full, (0 + i * 70, 10))
            else:
                self.screen.blit(self.heart_empty, (0 + i * 70, 10))

        # Utiliser self.total_time au lieu de settings.TOTAL_TIME
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, self.total_time - elapsed)
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
        import sprites  # Assure que sprites.load_sprites() a déjà été appelé

        self.spawned = 0
        self.next_spawn_time = time.time()
        self.enemies_to_spawn = count
        self.spawn_cooldown = cooldown

        # Définir les types d'ennemis selon la vague
        if self.wave == 1:
            self.wave_types = [Skeleton]
        elif self.wave == 2:
            self.wave_types = [Skeleton, Orc]
        else:
            self.wave_types = [Skeleton, Orc, Ghost]

        # Filtrer les types d'ennemis dont les sprites sont chargés
        valid_wave_types = []
        for enemy_type in self.wave_types:
            sprite_attr = f"{enemy_type.__name__.upper()}_SPRITES"
            enemy_sprites = getattr(sprites, sprite_attr, None)
            if enemy_sprites and "down" in enemy_sprites:
                valid_wave_types.append(enemy_type)
            else:
                print(f"Warning: {enemy_type.__name__} sprites not loaded or missing 'down', skipping this type")

        self.wave_types = valid_wave_types

        if not self.wave_types:
            print("Error: No valid enemy types to spawn! Make sure sprites are loaded.")

    def reset(self):
        if self.all_sprites:
            for sprite in self.all_sprites:
                sprite.kill()
        self.__init__()