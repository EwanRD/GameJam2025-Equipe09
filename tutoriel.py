import pygame
from settings import COLORS

class Tutoriel:
    def __init__(self, screen, title_font, button_font, colors, background, on_tutorial_complete):
        self.screen = screen
        self.title_font = title_font
        self.button_font = button_font
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.colors = colors
        self.background = background
        self.on_tutorial_complete = on_tutorial_complete
        
        self.current_page = 0
        self.total_pages = 4
        
        # Contenu du tutoriel
        self.tutorial_content = [
            {
                "title": "DÉPLACEMENT",
                "content": [
                    "Utilisez les touches suivantes pour vous déplacer :",
                    "",
                    "Z - Se déplacer vers le HAUT",
                    "Q - Se déplacer vers la GAUCHE", 
                    "S - Se déplacer vers le BAS",
                    "D - Se déplacer vers la DROITE",
                    "",
                    "Vous pouvez combiner les directions",
                    "pour vous déplacer en diagonal"
                ]
            },
            {
                "title": "COMBAT",
                "content": [
                    "Défendez-vous contre les ennemis :",
                    "",
                    "ESPACE - Tirer des flèches",
                    "",
                    "• Les flèches suivent votre direction de mouvement",
                    "• Chaque ennemi a des points de vie différents",
                    "• Attention aux projectiles ennemis !",
                    "",
                    "Récupérez des objets au sol pour vous aider"
                ]
            },
            {
                "title": "POUVOIR SPÉCIAL",
                "content": [
                    "La malédiction vous a donné un pouvoir:",
                    "",
                    "ENTRÉE - Activer votre pouvoir",
                    "",
                    "• Activable après 10 éliminations",
                    "• Vous rend temporairement invisible",
                    "",
                    "Récupérez des objets au sol pour vous aider"   
                ]
            },
            {
                "title": "OBJETS",
                "content": [
                    "Les ennemis peuvent lâcher des objets à leurs morts:",
                    "",
                    "• Coeur - Restaure 1 point de vie",
                    "• Botte - Augmente temporairement la vitesse",
                    "• Flèche en or - Augmente temporairement les dégâts",
                    "",
                    "Bonne chance dans votre aventure !"   
                ]
            }
        ]
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.next_page()
                elif event.key == pygame.K_ESCAPE:
                    self.skip_tutorial()
                elif event.key == pygame.K_BACKSPACE:  # Ajout de la touche retour
                    self.previous_page()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_pos = pygame.mouse.get_pos()
                    # Vérifier si on clique sur les boutons
                    if hasattr(self, 'next_button_rect') and self.next_button_rect.collidepoint(mouse_pos):
                        self.next_page()
                    elif hasattr(self, 'skip_button_rect') and self.skip_button_rect.collidepoint(mouse_pos):
                        self.skip_tutorial()
                    elif hasattr(self, 'back_button_rect') and self.back_button_rect.collidepoint(mouse_pos) and self.current_page > 0:
                        self.previous_page()
    
    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        else:
            self.on_tutorial_complete()
    
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
    
    def skip_tutorial(self):
        self.on_tutorial_complete()
    
    def draw(self):
        # Fond
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.colors['black'])
        
        # Overlay semi-transparent
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        screen_width, screen_height = self.screen.get_size()
        current_content = self.tutorial_content[self.current_page]
        
        # Titre de la page
        title_text = self.button_font.render(f"TUTORIEL - {current_content['title']}", True, self.colors['white'])
        title_rect = title_text.get_rect(center=(screen_width // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Indicateur de page
        page_text = self.small_font.render(f"Page {self.current_page + 1}/{self.total_pages}", True, self.colors['white'])
        page_rect = page_text.get_rect(center=(screen_width // 2, 180))
        self.screen.blit(page_text, page_rect)
        
        # Contenu
        y_offset = 250
        for line in current_content['content']:
            if line.strip():  # Si la ligne n'est pas vide
                # Différents styles selon le contenu
                if line.startswith("•"):
                    text_color = (200, 200, 255)  # Bleu clair pour les points
                elif any(key in line for key in ["Z -", "Q -", "S -", "D -", "ESPACE -", "ENTRÉE -"]):
                    text_color = (255, 255, 100)  # Jaune pour les touches
                else:
                    text_color = self.colors['white']
                
                text = self.small_font.render(line, True, text_color)
                text_rect = text.get_rect(center=(screen_width // 2, y_offset))
                self.screen.blit(text, text_rect)
            
            y_offset += 35
        
        # Boutons centrés
        button_y = screen_height - 200
        button_width = 200
        button_height = 50
        back_button_width = 120
        mouse_pos = pygame.mouse.get_pos()
        
        # Calcul des positions pour centrer les boutons
        spacing = 40
        total_width = back_button_width + spacing + button_width
        start_x = (screen_width - total_width) // 2
        
        # Bouton Retour - toujours affiché
        back_x = start_x
        self.back_button_rect = pygame.Rect(back_x, button_y, back_button_width, button_height)
        
        # Déterminer la couleur du bouton retour
        if self.current_page > 0:
            # Bouton actif
            back_button_color = self.colors['hover'] if self.back_button_rect.collidepoint(mouse_pos) else self.colors['button']
            back_text_color = self.colors['white']
        else:
            # Bouton grisé sur la première page
            back_button_color = (60, 60, 60)  # Gris foncé
            back_text_color = (120, 120, 120)  # Gris plus clair pour le texte
        
        pygame.draw.rect(self.screen, back_button_color, self.back_button_rect)
        pygame.draw.rect(self.screen, back_text_color, self.back_button_rect, 2)
        
        back_button_text = self.small_font.render("RETOUR", True, back_text_color)
        back_button_text_rect = back_button_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_button_text, back_button_text_rect)
        
        # Bouton Suivant/Commencer
        next_x = start_x + back_button_width + spacing
        next_text = "COMMENCER" if self.current_page == self.total_pages - 1 else "SUIVANT"
        self.next_button_rect = pygame.Rect(next_x, button_y, button_width, button_height)
        
        next_button_color = self.colors['hover'] if self.next_button_rect.collidepoint(mouse_pos) else self.colors['button']
        
        pygame.draw.rect(self.screen, next_button_color, self.next_button_rect)
        pygame.draw.rect(self.screen, self.colors['white'], self.next_button_rect, 2)
        
        next_button_text = self.small_font.render(next_text, True, self.colors['white'])
        next_button_text_rect = next_button_text.get_rect(center=self.next_button_rect.center)
        self.screen.blit(next_button_text, next_button_text_rect)
        
        # Bouton Passer (en bas à droite)
        skip_button_width = 120
        self.skip_button_rect = pygame.Rect(screen_width - skip_button_width - 30, screen_height - 80, skip_button_width, 40)
        skip_button_color = self.colors['hover'] if self.skip_button_rect.collidepoint(mouse_pos) else self.colors['button']
        
        pygame.draw.rect(self.screen, skip_button_color, self.skip_button_rect)
        pygame.draw.rect(self.screen, self.colors['white'], self.skip_button_rect, 2)
        
        skip_button_text = self.small_font.render("PASSER", True, self.colors['white'])
        skip_button_text_rect = skip_button_text.get_rect(center=self.skip_button_rect.center)
        self.screen.blit(skip_button_text, skip_button_text_rect)
        
        # Instructions en bas (mises à jour)
        instruction_text = "ESPACE/ENTRÉE: continuer • BACKSPACE: retour • ESC: passer"
        instruction = self.small_font.render(instruction_text, True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(screen_width // 2, screen_height - 50))
        self.screen.blit(instruction, instruction_rect)