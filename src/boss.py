import pygame
import time
import random
import sprites
from .utils import play_sound, get_direction_vector
import settings
from .projectiles.magic_missile import Magic_Missile


class Boss(pygame.sprite.Sprite):
    def __init__(self, human, projectiles):
        super().__init__()
        self.human = human
        self.image = sprites.BOSS_SPRITES[0]
        self.rect = self.image.get_rect(topleft=(632, 86))
        self.rect.inflate_ip(-25, -25)

        # Utiliser les stats de difficulté
        lich_stats = settings.get_current_lich_stats()
        self.health = lich_stats['health']
        self.max_health = self.health
        self.velocity = lich_stats['velocity']
        self.shoot_cooldown = lich_stats['cooldown']

        self.projectiles_direction = (0, 0)
        self.projectiles_group = projectiles

        self.last_teleport = 0
        self.last_shot_time = 0
        self.anim_timer = 0
        self.anim_speed = 30
        self.anim_index = 0

        self.state = "waiting"
        self.corners = [
            (65, 106),
            (1095, 106), 
            (65, 721),
            (1095, 721),
            (576, 382)
        ]
    
    def update(self):
        self.projectiles_direction = get_direction_vector(self.rect.x, self.rect.y, self.human.rect.x, self.human.rect.y, self.velocity)

        now = time.time()
        if self.state == "teleport":
            self.state = "waiting"
            self.last_teleport = now
        elif self.state == "waiting":
            # Animation idle
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(sprites.BOSS_SPRITES)
                self.image = sprites.BOSS_SPRITES[self.anim_index]
            if now - self.last_teleport > 4:
                self.state = "teleport"
                self.teleport()
        
        current_time = time.time()
        if current_time - self.last_shot_time > self.shoot_cooldown:
            self.shoot_at_player()
            self.last_shot_time = current_time


    def teleport(self):
        actual_position = self.rect.topleft
        self.x, self.y = random.choice(self.corners)
        self.rect.topleft = (self.x, self.y)
        while actual_position == self.rect.topleft:
            self.x, self.y = random.choice(self.corners)
            self.rect.topleft = (self.x, self.y)
        play_sound(sprites.LICH_TP_SOUND)

    def shoot_at_player(self):
        magic_missile = Magic_Missile(self.rect.center, self.projectiles_direction, settings.PLAYER_DOMMAGE)
        self.projectiles_group.add(magic_missile)

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            play_sound(sprites.DEATH_SOUND)
    
    def move(self, dx, dy, direction=None):
        None
    
    def draw_boss_health_bar(self, screen, x=10, y=80):
        "Draw boss health bar with individual health points"
        bar_width = 400
        bar_height = 25
        border_thickness = 3
        segments = self.max_health  # each HP is a segment

        # Shadow
        shadow_offset = 2
        pygame.draw.rect(screen, (0, 0, 0),
                        (x + shadow_offset, y + shadow_offset, bar_width, bar_height),
                        border_radius=8)

        # Border
        pygame.draw.rect(screen, (120, 0, 0), (x, y, bar_width, bar_height),
                        border_thickness, border_radius=8)

        # Background
        pygame.draw.rect(screen, (25, 25, 35),
                        (x + border_thickness, y + border_thickness,
                        bar_width - 2*border_thickness, bar_height - 2*border_thickness),
                        border_radius=5)

        # Draw segments
        segment_width = (bar_width - 2*border_thickness) / segments
        for i in range(segments):
            segment_x = x + border_thickness + i * segment_width
            if i < self.health:
                # Fill color based on remaining health ratio
                ratio = self.health / self.max_health
                if ratio > 0.6:
                    color = (0, 255, 0)
                elif ratio > 0.3:
                    color = (255, 165, 0)
                else:
                    color = (255, 0, 0)
            else:
                # Empty segment
                color = (50, 50, 50)
            pygame.draw.rect(screen, color,
                            (segment_x, y + border_thickness, segment_width - 1, bar_height - 2*border_thickness))
