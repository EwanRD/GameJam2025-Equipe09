import pygame
from settings import COLORS

class Difficulty:
    def __init__(self, screen, title_font, button_font, colors, background, on_difficulty_selected):
        self.screen = screen
        self.title_font = title_font
        self.button_font = button_font
        self.colors = colors
        self.background = background
        self.on_difficulty_selected = on_difficulty_selected
        self.buttons = []
        
        # Créer les boutons de difficulté
        screen_width, screen_height = screen.get_size()
        button_width, button_height = 300, 80
        
        # Position des boutons
        easy_y = screen_height // 2 - 100
        normal_y = screen_height // 2
        hard_y = screen_height // 2 + 100
        back_y = screen_height // 2 + 200
        
        # Boutons avec leurs descriptions
        self.buttons = [
            {
                'text': 'FACILE',
                'rect': pygame.Rect(screen_width // 2 - button_width // 2, easy_y, button_width, button_height),
                'difficulty': 'easy',
                'hovered': False
            },
            {
                'text': 'NORMAL',
                'rect': pygame.Rect(screen_width // 2 - button_width // 2, normal_y, button_width, button_height),
                'difficulty': 'normal',
                'hovered': False
            },
            {
                'text': 'DIFFICILE',
                'rect': pygame.Rect(screen_width // 2 - button_width // 2, hard_y, button_width, button_height),
                'difficulty': 'hard',
                'hovered': False
            },
            {
                'text': 'RETOUR',
                'rect': pygame.Rect(screen_width // 2 - button_width // 2, back_y, button_width, button_height),
                'difficulty': 'back',
                'hovered': False
            }
        ]
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Vérifier le survol des boutons
        for button in self.buttons:
            button['hovered'] = button['rect'].collidepoint(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    for button in self.buttons:
                        if button['rect'].collidepoint(mouse_pos):
                            self.on_difficulty_selected(button['difficulty'])
    
    def draw(self):
        # Fond
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.colors['black'])
        
        # Overlay semi-transparent
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Titre (font agrandie)
        title_font_large = pygame.font.SysFont("Arial", 48)
        title_text = title_font_large.render("CHOISIR LA DIFFICULTÉ", True, self.colors['white'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(title_text, title_rect)
        
        # Dessiner les boutons
        for button in self.buttons:
            # Couleur du bouton selon le survol
            button_color = self.colors['hover'] if button['hovered'] else self.colors['button']
            
            # Dessiner le bouton
            pygame.draw.rect(self.screen, button_color, button['rect'])
            pygame.draw.rect(self.screen, self.colors['white'], button['rect'], 2)
            
            # Texte du bouton
            button_text = self.button_font.render(button['text'], True, self.colors['white'])
            button_text_rect = button_text.get_rect(center=button['rect'].center)
            self.screen.blit(button_text, button_text_rect)
