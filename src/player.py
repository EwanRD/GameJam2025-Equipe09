import pygame
from .utils import play_sound
import settings 
import sprites 
from .entity import Entity
import time
from src.projectiles.arrow import Arrow
from .pouvoir import Pouvoir

class Player(Entity):
    def __init__(self, x, y, projectiles_group, walls):
        sprite = sprites.PLAYER_SPRITES
        super().__init__(x, y, sprite, settings.PLAYER_SPEED)
        self.projectiles_group = projectiles_group
        self.last_shot_time = 0
        self.walls = walls
        self.speed = settings.PLAYER_SPEED
        self.speed_boost_end = 0
        self.projectile_direction = settings.DIRECTION.B.value
        self.projectile_sprite = settings.ARROW_DIRECTION.B.value
        self.damage_boost_count = 0
        self.invisibility = Pouvoir(self)

        # Utiliser les stats de difficulté
        player_stats = settings.get_current_player_stats()
        self.health = player_stats['health']
        self.max_health = player_stats['health']  # Nouveau : HP maximum selon la difficulté
        self.projectile_damage = player_stats['damage']
        self.shoot_cooldown = player_stats['cooldown']

        # Invincibilité temporaire après dégâts
        self.invincible_after_damage = False
        self.invincibility_end_time = 0
        self.invincibility_duration = 2.0
        self.blink_timer = 0
        self.blink_interval = 0.1
        self.visible = True

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        self.invisibility.update(keys)

        # Gestion de l'invincibilité temporaire
        if self.invincible_after_damage:
            if time.time() > self.invincibility_end_time:
                # Fin de l'invincibilité
                self.invincible_after_damage = False
                self.visible = True
            else:
                # Gestion du clignotement pendant l'invincibilité
                if time.time() - self.blink_timer > self.blink_interval:
                    self.visible = not self.visible
                    self.blink_timer = time.time()

        # Boost de vitesse temporaire
        if self.speed_boost_end and time.time() > self.speed_boost_end:
            self.speed = settings.PLAYER_SPEED
            self.speed_boost_end = 0

        # Mouvement horizontal
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed

        # Mouvement vertical
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        # Détermination direction projectile
        if dx < 0 and dy < 0:
            self.projectile_direction = settings.DIRECTION.HG.value
            self.projectile_sprite = settings.ARROW_DIRECTION.HG.value
        elif dx > 0 and dy < 0:
            self.projectile_direction = settings.DIRECTION.HD.value
            self.projectile_sprite = settings.ARROW_DIRECTION.HD.value
        elif dx < 0 and dy > 0:
            self.projectile_direction = settings.DIRECTION.BG.value
            self.projectile_sprite = settings.ARROW_DIRECTION.BG.value
        elif dx > 0 and dy > 0:
            self.projectile_direction = settings.DIRECTION.BD.value
            self.projectile_sprite = settings.ARROW_DIRECTION.BD.value
        elif dx < 0:
            self.projectile_direction = settings.DIRECTION.G.value
            self.projectile_sprite = settings.ARROW_DIRECTION.G.value
        elif dx > 0:
            self.projectile_direction = settings.DIRECTION.D.value
            self.projectile_sprite = settings.ARROW_DIRECTION.D.value
        elif dy < 0:
            self.projectile_direction = settings.DIRECTION.H.value
            self.projectile_sprite = settings.ARROW_DIRECTION.H.value
        elif dy > 0:
            self.projectile_direction = settings.DIRECTION.B.value
            self.projectile_sprite = settings.ARROW_DIRECTION.B.value

        # Tir
        if keys[pygame.K_SPACE]:
            current_time = time.time()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = current_time

        # Déplacement
        self.move(dx, dy)

    def shoot(self):
        arrow = Arrow(self.rect.center, self.projectile_direction, settings.PLAYER_DOMMAGE,self.projectile_sprite, self)
        play_sound(sprites.SHOOT_SOUND)
        self.projectiles_group.add(arrow)

    def take_damage(self):
        # Si invisible ou invincible temporairement, ne pas prendre de dégâts
        if not self.invisibility.can_take_damage() or self.invincible_after_damage:
            return

        self.health -= 1

        # Activer l'invincibilité temporaire après avoir pris des dégâts
        self.invincible_after_damage = True
        self.invincibility_end_time = time.time() + self.invincibility_duration
        self.visible = True

        if self.health <= 0:
            self.kill()
            print("Player has died")

    def add_kill(self):
        """Méthode pour ajouter un kill depuis l'extérieur"""
        self.invisibility.add_kill()

    def is_invincible(self):
        """Méthode utilitaire pour vérifier si le joueur est invincible"""
        return not self.invisibility.can_take_damage() or self.invincible_after_damage