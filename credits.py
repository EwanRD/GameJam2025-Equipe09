import pygame

class Credits:
    def __init__(self, screen, title_font, text_font, colors, back_action, bg_image=None):
        self.screen = screen
        self.title_font = title_font       # Police des titres (Team, Assets, Sons)
        self.text_font = text_font         # Police du texte normal
        self.colors = colors
        self.back_action = back_action
        self.bg_image = bg_image

        # Texte des crédits avec flag titre et espacement après
        self.lines = [
            ("Equipe", True, 20),
            ("RENE-DAGUET Ewan : Chef de projet", False, 0),
            ("BENHADADA Tejeddine : Narrateur", False, 0),
            ("DASSAC Noah : Designer", False, 0),
            ("MICHEL Eliot : Maître du temps", False, 0),
            ("MBELO NDRIAMANAMPY Manohisoa : Secrétaire", False, 30),
            ("Assets et ressources :", True, 20),
            ("https://www.rpg-maker.fr/ressources/vxchar/Monster2.png-par-MonkeySoul.png", False, 0),
            ("https://www.rpg-maker.fr/ressources/vxchar/down2chara.png",  False, 0),
            ("https://www.rpg-maker.fr/ressources/vxchar/$darkrufus.png",  False, 0),
            ("https://nicolemariet.itch.io/pixel-heart-animation-32x32-16x16-freebie", False, 0),
            ("https://www.reddit.com/r/PixelArt/comments/cbuzjc/crypt/#lightbox", False, 0),
            ("https://www.rpg-maker.fr/ressources/battleanims/invocs/14751_1114538629.png", False, 0),
            ("https://pixel-poem.itch.io/dungeon-assetpuck", False, 0),
            ("https://www.mapeditor.org", False, 30),
            ("Sons:", True, 20),
            ("https://opengameart.org/content/the-crypt", False, 0),
            ("https://opengameart.org/content/bow-arrow-shot", False, 0),
            ("https://opengameart.org/content/game-over-soundold-school", False, 0),
            ("https://pixabay.com/sound-effects/search/hurt/",  False, 0),
            ("https://opengameart.org/content/boss-battle-2-8-bit-re-upload", False, 0),
            ("https://opengameart.org/content/retro-monster-roar", False, 30),
            ("https://opengameart.org/content/spell-4-fire", False, 30)
        ]

        self.scroll_y = 0
        self.scroll_speed = 0.5 # vitesse automatique
        self.line_height = 50
        self.title_spacing = 30

        # Bouton retour
        self.back_rect = pygame.Rect(20, 20, 120, 40)

        # Calcul hauteur totale
        self.total_height = 0
        for text, is_title, extra in self.lines:
            if is_title:
                self.total_height += self.line_height + self.title_spacing
            else:
                self.total_height += self.line_height + extra

    def reset(self):
        self.scroll_y = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.back_action()

    def draw(self):
        # Background
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((255, 255, 255))

        # Scroll automatique
        self.scroll_y += self.scroll_speed

        # Loop quand le scroll dépasse le texte
        if self.scroll_y > self.total_height:
            self.scroll_y = 0

        # Affichage des lignes
        y = 100 - self.scroll_y  # on commence au top et on descend
        for text, is_title, extra in self.lines:
            surf = self.title_font.render(text, True, (139, 69, 19)) if is_title else self.text_font.render(text, True, (0, 0, 0))
            self.screen.blit(surf, surf.get_rect(center=(self.screen.get_width() // 2, y)))
            y += self.line_height
            if is_title:
                y += self.title_spacing
            y += extra

        # Bouton retour avec hover
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.back_rect.collidepoint(mouse):
            color = (200, 200, 200)
            if click[0]:
                self.back_action()
        else:
            color = self.colors['button']
        pygame.draw.rect(self.screen, color, self.back_rect, border_radius=15)
        back_text = self.text_font.render("Retour", True, (0, 0, 0))
        self.screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))
