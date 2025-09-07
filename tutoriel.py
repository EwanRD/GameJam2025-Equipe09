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
        
        # Animation du personnage
        try:
            # Charger les deux images du personnage
            self.character_image1 = pygame.image.load("assets/images/blanchon2.png").convert_alpha()
            self.character_image2 = pygame.image.load("assets/images/blanchon1.png").convert_alpha()
            
            # Redimensionner les images si nécessaire
            desired_size = (120, 120)
            self.character_image1 = pygame.transform.scale(self.character_image1, desired_size)
            self.character_image2 = pygame.transform.scale(self.character_image2, desired_size)
            
            self.character_images = [self.character_image1, self.character_image2]
            self.has_character_images = True
        except pygame.error:
            print("Impossible de charger les images du personnage")
            self.has_character_images = False
        
        # Variables pour l'animation
        self.current_character_frame = 0
        self.last_animation_time = 0
        self.animation_speed = 600  # Temps en millisecondes entre chaque frame
        
        # Variables pour l'animation de "parole"
        self.is_talking = True
        self.talk_pause_timer = 0
        self.talk_duration = 2000  # Durée de parole en ms
        self.pause_duration = 500  # Durée de pause en ms
        
        # Position du personnage
        self.character_x = 30
        
        # Contenu du tutoriel avec dialogues du personnage
        self.tutorial_content = [
            {
                "title": "DÉPLACEMENT",
                "dialogue": "Salut ! Je vais t'apprendre à te déplacer !",
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
                "dialogue": "Maintenant, apprenons à nous battre !",
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
                "dialogue": "Tu as un pouvoir secret très utile !",
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
                "dialogue": "N'oublie pas les objets, ils sont précieux !",
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
    
    def update_animation(self):
        """Met à jour l'animation du personnage"""
        current_time = pygame.time.get_ticks()
        
        if self.has_character_images:
            # Animation de parole/pause
            if self.is_talking:
                # Le personnage "parle" - animation rapide
                if current_time - self.last_animation_time >= self.animation_speed:
                    self.current_character_frame = (self.current_character_frame + 1) % len(self.character_images)
                    self.last_animation_time = current_time
                
                # Vérifier si la durée de parole est écoulée
                if current_time - self.talk_pause_timer >= self.talk_duration:
                    self.is_talking = False
                    self.talk_pause_timer = current_time
                    self.current_character_frame = 0  # Image de repos
            else:
                # Le personnage fait une pause - reste sur la première image
                if current_time - self.talk_pause_timer >= self.pause_duration:
                    self.is_talking = True
                    self.talk_pause_timer = current_time

    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.next_page()
                elif event.key == pygame.K_ESCAPE:
                    self.skip_tutorial()
                elif event.key == pygame.K_BACKSPACE:
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
            # Redémarrer l'animation de parole pour la nouvelle page
            self.is_talking = True
            self.talk_pause_timer = pygame.time.get_ticks()
        else:
            self.on_tutorial_complete()
    
    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            # Redémarrer l'animation de parole pour la page précédente
            self.is_talking = True
            self.talk_pause_timer = pygame.time.get_ticks()
    
    def skip_tutorial(self):
        self.on_tutorial_complete()
    
    def draw_speech_bubble(self, text, character_rect):
        """Dessine une bulle de dialogue au-dessus du personnage"""
        if not text:
            return
            
        # Créer le texte de la bulle
        bubble_font = pygame.font.SysFont("Arial", 20)
        text_surface = bubble_font.render(text, True, (50, 50, 50))
        text_rect = text_surface.get_rect()
        
        # Dimensions de la bulle
        bubble_padding = 15
        bubble_width = text_rect.width + bubble_padding * 2
        bubble_height = text_rect.height + bubble_padding * 2
        
        # Position de la bulle (décalée vers la droite et plus haut)
        bubble_x = character_rect.centerx + 40 
        bubble_y = character_rect.top - bubble_height - 80
        
        # S'assurer que la bulle reste à l'écran
        screen_width = self.screen.get_width()
        if bubble_x < 10:
            bubble_x = 10
        elif bubble_x + bubble_width > screen_width - 10:
            bubble_x = screen_width - bubble_width - 10
        
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        
        # Dessiner la bulle
        pygame.draw.rect(self.screen, (255, 255, 255), bubble_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), bubble_rect, 2, border_radius=10)
        
        # Position de la pointe
        mouth_x = character_rect.right + -30
        mouth_y = character_rect.centery + -10 
        
        # Dessiner la petite flèche de la bulle
        arrow_tip = (mouth_x, mouth_y)
        arrow_left = (bubble_rect.left + 15, bubble_rect.bottom)
        arrow_right = (bubble_rect.left + 35, bubble_rect.bottom)
        pygame.draw.polygon(self.screen, (255, 255, 255), [arrow_tip, arrow_left, arrow_right])
        pygame.draw.lines(self.screen, (200, 200, 200), False, [arrow_left, arrow_tip, arrow_right], 2)
        
        # Dessiner le texte dans la bulle
        text_x = bubble_rect.centerx - text_rect.width // 2
        text_y = bubble_rect.centery - text_rect.height // 2
        self.screen.blit(text_surface, (text_x, text_y))
    
    def draw(self):
        # Mettre à jour l'animation automatiquement
        self.update_animation()
        
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
        
        # Dessiner le personnage animé en bas à gauche
        if self.has_character_images:
            character_y = screen_height - 150
            current_image = self.character_images[self.current_character_frame]
            character_rect = current_image.get_rect()
            character_rect.x = self.character_x
            character_rect.y = character_y
            
            self.screen.blit(current_image, character_rect)
            
            # Dessiner la bulle de dialogue
            self.draw_speech_bubble(current_content['dialogue'], character_rect)
        
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
        
        # Bouton Retour
        back_x = start_x
        self.back_button_rect = pygame.Rect(back_x, button_y, back_button_width, button_height)
        
        if self.current_page > 0:
            back_button_color = self.colors['hover'] if self.back_button_rect.collidepoint(mouse_pos) else self.colors['button']
            back_text_color = self.colors['white']
        else:
            back_button_color = (60, 60, 60)
            back_text_color = (120, 120, 120)
        
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
        
        # Bouton Passer
        skip_button_width = 120
        self.skip_button_rect = pygame.Rect(screen_width - skip_button_width - 30, screen_height - 80, skip_button_width, 40)
        skip_button_color = self.colors['hover'] if self.skip_button_rect.collidepoint(mouse_pos) else self.colors['button']
        
        pygame.draw.rect(self.screen, skip_button_color, self.skip_button_rect)
        pygame.draw.rect(self.screen, self.colors['white'], self.skip_button_rect, 2)
        
        skip_button_text = self.small_font.render("PASSER", True, self.colors['white'])
        skip_button_text_rect = skip_button_text.get_rect(center=self.skip_button_rect.center)
        self.screen.blit(skip_button_text, skip_button_text_rect)
        
        # Instructions en bas
        instruction_text = "ESPACE/ENTRÉE: continuer • BACKSPACE: retour • ESC: passer"
        instruction = self.small_font.render(instruction_text, True, (150, 150, 150))
        instruction_rect = instruction.get_rect(center=(screen_width // 2, screen_height - 50))
        self.screen.blit(instruction, instruction_rect)