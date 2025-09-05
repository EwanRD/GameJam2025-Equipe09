import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from menu import Button  # on réutilise ton bouton


class QuitPopup:
    """
    Popup de confirmation. on_yes et on_no sont des callbacks.
    """
    def __init__(self, screen, font, colors, origin_state, on_yes, on_no):
        self.screen = screen
        self.font = font
        self.colors = colors
        self.origin_state = origin_state
        self.on_yes = on_yes
        self.on_no = on_no

        # boutons
        self.oui_button = Button("Oui", (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2 + 50, 120, 50), font, colors, self._yes)
        self.non_button = Button("Non", (SCREEN_WIDTH//2 + 110, SCREEN_HEIGHT//2 + 50, 120, 50), font, colors, self._no)

        # petit drapeau anti-reclic (pour éviter plusieurs triggers si l'utilisateur garde le clic)
        self._mouse_was_down = False

    def _yes(self):
        # wrapper pour s'assurer qu'on ne déclenche qu'une fois
        self.on_yes()

    def _no(self):
        self.on_no()

    def draw(self):
        # Fond semi-transparent (le popup gère son overlay)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Fenêtre popup
        popup_rect = pygame.Rect(0, 0, 500, 250)
        popup_rect.center = (SCREEN_WIDTH// 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(self.screen, self.colors["button"], popup_rect, border_radius=15)

        # Texte
        text = self.font.render("Voulez-vous vraiment quitter ?", True, self.colors["white"])
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))

        # Dessin des boutons (Button.draw() gère le click directement)
        self.oui_button.draw(self.screen)
        self.non_button.draw(self.screen)
