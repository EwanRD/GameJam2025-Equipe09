import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Button:
    def __init__(self, text, rect, font, colors, action=None):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.font = font
        self.colors = colors
        self.action = action
        self.hovered = False

    def draw(self, screen):
        color = self.colors["hover"] if self.hovered else self.colors["button"]
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        text_surf = self.font.render(self.text, True, self.colors["white"])
        screen.blit(text_surf, text_surf.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()


class Menu:
    def __init__(self, screen, title, title_font, button_font, colors, background=None, with_overlay=False):
        self.screen = screen
        self.title = title
        self.title_font = title_font
        self.button_font = button_font
        self.colors = colors
        self.background = background
        self.buttons = []
        self.with_overlay = with_overlay

    def add_button(self, text, center, size, action):
        rect = pygame.Rect(0, 0, size[0], size[1])
        rect.center = center
        button = Button(text, rect, self.button_font, self.colors, action)
        self.buttons.append(button)

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        if self.with_overlay:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(self.colors["overlay"])
            self.screen.blit(overlay, (0, 0))
        if self.title:
            titre_surf = self.title_font.render(self.title, True, self.colors["brown"])
            self.screen.blit(titre_surf, titre_surf.get_rect(center=(SCREEN_WIDTH // 2 - 5, 250)))
        for button in self.buttons:
            button.draw(self.screen)


class QuitPopup:
    def __init__(self, screen, font, colors, origin_state, on_yes, on_no):
        self.screen = screen
        self.font = font
        self.colors = colors
        self.origin_state = origin_state
        self.on_yes = on_yes
        self.on_no = on_no

        self.oui_button = Button("Oui", (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 150, 50), font, colors, self.on_yes)
        self.non_button = Button("Non", (SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2 + 50, 150, 50), font, colors, self.on_no)

    def handle_events(self, events):
        for event in events:
            self.oui_button.handle_event(event)
            self.non_button.handle_event(event)

    def draw(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(0, 0, 500, 250)
        popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, self.colors["button"], popup_rect, border_radius=15)

        text = self.font.render("Voulez-vous vraiment quitter ?", True, self.colors["white"])
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))

        self.oui_button.draw(self.screen)
        self.non_button.draw(self.screen)
