import pygame
import time
import sprites
from .utils import play_sound

class Pouvoir:
    def __init__(self, player):
        self.player = player
        self.kill_count = 0
        self.invisible = False
        self.invisibility_end_time = 0
        self.invisibility_duration = 5.0
        self.invisibility_available = False
        self.last_enter_press = 0
        self.enter_cooldown = 0.2
    
    def update(self, keys):
        """Met à jour le pouvoir d'invisibilité"""
        # Vérifier si l'invisibilité est finie
        if self.invisible and time.time() > self.invisibility_end_time:
            self.invisible = False

        # Vérifier si le pouvoir est disponible
        if self.kill_count >= 10:
            self.invisibility_available = True

        # Activation avec Enter
        if keys[pygame.K_RETURN]:
            current_time = time.time()
            if (current_time - self.last_enter_press > self.enter_cooldown and 
                self.invisibility_available and not self.invisible):
                self.activate()
                self.last_enter_press = current_time
    
    def activate(self):
        """Active le pouvoir d'invisibilité"""
        if self.invisibility_available and not self.invisible:
            play_sound(sprites.PLAYER_POWER_SOUND)
            self.invisible = True
            self.invisibility_end_time = time.time() + self.invisibility_duration
            self.invisibility_available = False
            self.kill_count = 0  # Reset le compteur

    def add_kill(self):
        """Ajoute un kill au compteur - SEULEMENT si pas invisible"""
        if not self.invisible:  # Ne pas compter les kills si invisible
            self.kill_count += 1
            print(f"Kills: {self.kill_count}/10")
            if self.kill_count >= 10 and not self.invisibility_available:
                self.invisibility_available = True
    
    def can_take_damage(self):
        """Retourne si le joueur peut prendre des dégâts"""
        return not self.invisible
    
    def should_enemies_follow(self):
        """Retourne si les ennemis doivent suivre le joueur"""
        return not self.invisible
    
    def draw_power_bar(self, screen, x=10, y=80):  
        """Dessine la barre de progression du pouvoir"""
        bar_width = 220
        bar_height = 25
        border_thickness = 3

        # Calculer la progression selon l'état
        if self.invisible:
            # Pendant l'invisibilité : barre qui se vide selon le temps restant
            remaining_time = max(0, self.invisibility_end_time - time.time())
            progress = remaining_time / self.invisibility_duration
            bar_state = "invisible"
        elif self.invisibility_available:
            # Pouvoir disponible
            progress = 1.0
            bar_state = "ready"
        else:
            # Accumulation des kills
            progress = min(self.kill_count / 10.0, 1.0)
            bar_state = "charging"

        fill_width = int((bar_width - 2*border_thickness) * progress)

        # Dessiner l'ombre de la barre
        shadow_offset = 2
        pygame.draw.rect(screen, (0, 0, 0), 
                        (x + shadow_offset, y + shadow_offset, bar_width, bar_height), 
                        border_radius=8)

        # Dessiner le contour principal avec dégradé
        border_color = (120, 120, 150) if bar_state != "ready" else (200, 255, 200)
        pygame.draw.rect(screen, border_color, 
                        (x, y, bar_width, bar_height), 
                        border_thickness, border_radius=8)

        # Fond de la barre
        bg_color = (25, 25, 35)
        pygame.draw.rect(screen, bg_color, 
                        (x + border_thickness, y + border_thickness, 
                         bar_width - 2*border_thickness, bar_height - 2*border_thickness), 
                        border_radius=5)

        # Couleurs et effets selon l'état
        if bar_state == "invisible":
            # Bleu cyan clignotant pendant l'invisibilité
            pulse = 0.7 + 0.3 * abs(pygame.time.get_ticks() % 600 - 300) / 300
            fill_color = (int(0 * pulse), int(200 * pulse), int(255 * pulse))
            
        elif bar_state == "ready":
            # Vert éclatant avec effet de pulsation quand prêt
            pulse = 0.6 + 0.4 * abs(pygame.time.get_ticks() % 800 - 400) / 400
            fill_color = (int(50 * pulse), int(255 * pulse), int(100 * pulse))
            
            # Effet de brillance qui traverse la barre
            shine_pos = (pygame.time.get_ticks() * 0.15) % (bar_width * 1.5)
            if 0 <= shine_pos <= bar_width:
                shine_width = 40
                for i in range(shine_width):
                    alpha = int(80 * (1 - abs(i - shine_width//2) / (shine_width//2)))
                    if alpha > 0:
                        shine_x = int(x + shine_pos - shine_width//2 + i)
                        if x <= shine_x <= x + bar_width:
                            pygame.draw.line(screen, (255, 255, 255, alpha), 
                                           (shine_x, y + 2), (shine_x, y + bar_height - 2))
                                           
        else:  # charging
            # Gradient progressif rouge -> orange -> jaune -> vert
            if progress < 0.3:
                ratio = progress / 0.3
                fill_color = (255, int(100 * ratio), 0)
            elif progress < 0.6:
                ratio = (progress - 0.3) / 0.3
                fill_color = (255, int(100 + 100 * ratio), 0)
            elif progress < 0.9:
                ratio = (progress - 0.6) / 0.3
                fill_color = (int(255 - 100 * ratio), 200, int(50 * ratio))
            else:
                ratio = (progress - 0.9) / 0.1
                fill_color = (int(155 - 155 * ratio), int(200 + 55 * ratio), int(50 + 50 * ratio))

        # Dessiner le remplissage principal
        if fill_width > 4:
            fill_rect = (x + border_thickness, y + border_thickness, 
                        fill_width, bar_height - 2*border_thickness)
            pygame.draw.rect(screen, fill_color, fill_rect, border_radius=4)
            
            # Effet de surbrillance en haut de la barre
            highlight_height = (bar_height - 2*border_thickness) // 3
            highlight_color = tuple(min(255, int(c * 1.3)) for c in fill_color)
            highlight_rect = (fill_rect[0], fill_rect[1], fill_rect[2], highlight_height)
            pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=4)

        # Segments pour visualiser les kills individuels (seulement en mode charging)
        if bar_state == "charging":
            segment_width = (bar_width - 2*border_thickness) / 10
            for i in range(1, 10):
                segment_x = x + border_thickness + i * segment_width
                segment_color = (80, 80, 80) if i > self.kill_count else (40, 40, 40)
                pygame.draw.line(screen, segment_color, 
                                (segment_x, y + border_thickness + 2), 
                                (segment_x, y + bar_height - border_thickness - 2), 1)

        # Message d'instruction simple
        if self.invisibility_available and not self.invisible:
            # Animation du message simple
            pulse = 0.8 + 0.2 * abs(pygame.time.get_ticks() % 1000 - 500) / 500
            
            instruction_font = pygame.font.SysFont(None, 22, bold=True)
            instruction_text = instruction_font.render("Appuyez sur ENTRÉE pour activer", 
                                                     True, (int(150 * pulse), int(255 * pulse), int(150 * pulse)))
            
            # Positionner le texte sous la barre, centré
            text_rect = instruction_text.get_rect(center=(x + bar_width // 2, y + bar_height + 15))
            screen.blit(instruction_text, text_rect)