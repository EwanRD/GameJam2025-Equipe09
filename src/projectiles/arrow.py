import pygame
import sprites
import settings
from src.utils import play_sound
from src.projectiles.projectile import Projectile

class Arrow(Projectile):
    def __init__(self, position, velocity, damage, sprite, shooter):
        super().__init__(position, velocity, damage)
        
        # Vérifier si le joueur a un power-up actif pour utiliser les flèches dorées
        if hasattr(shooter, "damage_boost_count") and shooter.damage_boost_count > 0:
            # Convertir le sprite normal en sprite doré
            golden_sprite = self._get_golden_sprite(sprite)
            self.image = pygame.image.load(golden_sprite).convert_alpha()
        else:
            self.image = pygame.image.load(sprite).convert_alpha()
            
        self.rect = self.image.get_rect(topleft=position)
        self.shooter = shooter
    
    def _get_golden_sprite(self, normal_sprite):
        """Convertit un sprite de flèche normale en sprite de flèche dorée"""
        # Mapping des sprites normaux vers les sprites dorés
        sprite_mapping = {
            settings.ARROW_DIRECTION.H.value: settings.GOLDARROW_DIRECTION.H.value,
            settings.ARROW_DIRECTION.B.value: settings.GOLDARROW_DIRECTION.B.value,
            settings.ARROW_DIRECTION.G.value: settings.GOLDARROW_DIRECTION.G.value,
            settings.ARROW_DIRECTION.D.value: settings.GOLDARROW_DIRECTION.D.value,
            settings.ARROW_DIRECTION.HG.value: settings.GOLDARROW_DIRECTION.HG.value,
            settings.ARROW_DIRECTION.HD.value: settings.GOLDARROW_DIRECTION.HD.value,
            settings.ARROW_DIRECTION.BG.value: settings.GOLDARROW_DIRECTION.BG.value,
            settings.ARROW_DIRECTION.BD.value: settings.GOLDARROW_DIRECTION.BD.value,
        }
        
        # Retourner le sprite doré correspondant, ou le sprite normal si pas trouvé
        return sprite_mapping.get(normal_sprite, normal_sprite)
    
    def on_hit(self, target):
        # Utiliser les dégâts basés sur la difficulté
        base_damage = settings.get_current_player_stats()['damage']
        
        # Si le joueur a un boost de dégâts actif, utiliser les dégâts boostés
        if hasattr(self.shooter, "damage_boost_count") and self.shooter.damage_boost_count > 0:
            damage_to_deal = self.shooter.projectile_damage
            self.shooter.damage_boost_count -= 1
            if self.shooter.damage_boost_count == 0:
                self.shooter.projectile_damage = base_damage
        else:
            damage_to_deal = base_damage
            
        target.take_damage(damage_to_deal)
        play_sound(sprites.HIT_SOUND)
    
    def update(self, dt=2):
        self.position += self.velocity * dt
        self.rect.topleft = self.position