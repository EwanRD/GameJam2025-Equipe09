import pygame
import sys
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FPS, DIFFICULTY_LEVEL, set_difficulty
from menu import Menu, QuitPopup
from credits import Credits
from game import Game
from difficulty import Difficulty

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TOMB BOUND")

    title_font = pygame.font.Font("assets/the_centurion/The Centurion .ttf", 78)
    button_font = pygame.font.SysFont("Arial", 32)

    # Backgrounds
    background = pygame.image.load("assets/images/screen.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    credits_bg = pygame.image.load("assets/images/jpeg(3)")
    credits_bg = pygame.transform.scale(credits_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Cinématique
    cinematic_images = [
        pygame.transform.scale(pygame.image.load("assets/images/cinematique1.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(pygame.image.load("assets/images/cinematique2.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(pygame.image.load("assets/images/cinematique3.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    ]
    cinematic_index = 0
    cinematic_played = False

    # États (ajout de l'état difficulté)
    STATE_MENU = "menu"
    STATE_DIFFICULTY = "difficulty"
    STATE_CINEMATIC = "cinematic"
    STATE_GAME = "game"
    STATE_PAUSE = "pause"
    STATE_CREDITS = "credits"
    STATE_QUIT = "quit_popup"
    state = STATE_MENU

    # Jeu
    game = Game()

    # Menus
    main_menu = Menu(screen, " ", title_font, button_font, COLORS, background)
    pause_menu = Menu(screen, "Pause", title_font, button_font, COLORS, background=None, with_overlay=True)
    quit_popup = None

    # Credits
    credits_screen = Credits(screen, title_font, button_font, COLORS, lambda: set_state(STATE_MENU), credits_bg)

    # Menu de difficulté (nouveau)
    def on_difficulty_selected(difficulty):
        if difficulty == 'back':
            set_state(STATE_MENU)
        else:
            # Définir la difficulté selon le choix
            if difficulty == 'easy':
                set_difficulty(DIFFICULTY_LEVEL.EASY)
            elif difficulty == 'normal':
                set_difficulty(DIFFICULTY_LEVEL.NORMAL)
            elif difficulty == 'hard':
                set_difficulty(DIFFICULTY_LEVEL.HARD)
            
            # Démarrer le jeu
            start_game()

    difficulty_menu = Difficulty(screen, title_font, button_font, COLORS, background, on_difficulty_selected)

    # Fonctions pour changer d'état
    def set_state(new_state):
        nonlocal state, cinematic_index
        state = new_state
        if new_state == STATE_CINEMATIC:
            cinematic_index = 0
        if new_state == STATE_CREDITS:
            credits_screen.reset()
        if new_state == STATE_GAME:
            game.__init__()  # Réinitialise le jeu si on revient du menu

    def start_game():
        nonlocal cinematic_played
        if not cinematic_played:
            cinematic_played = True
            set_state(STATE_CINEMATIC)
        else:
            set_state(STATE_GAME)

    def show_difficulty_menu():
        set_state(STATE_DIFFICULTY)

    def show_credits():
        set_state(STATE_CREDITS)

    def resume_game():
        set_state(STATE_GAME)

    def ask_quit():
        nonlocal state, quit_popup
        origin = state
        def on_yes():
            if origin == STATE_MENU:
                pygame.quit()
                sys.exit()
            else:
                game.__init__()
                set_state(STATE_MENU)
        def on_no():
            set_state(origin)
        quit_popup = QuitPopup(screen, button_font, COLORS, origin, on_yes, on_no)
        state = STATE_QUIT

    # Ajouter boutons (modifié pour aller au menu de difficulté)
    main_menu.add_button("Jouer", (SCREEN_WIDTH // 2, 400), (240, 70), show_difficulty_menu)  # Changé ici
    main_menu.add_button("Crédits", (SCREEN_WIDTH // 2, 500), (240, 70), show_credits)
    main_menu.add_button("Quitter", (SCREEN_WIDTH // 2, 600), (240, 70), ask_quit)

    pause_menu.add_button("Continuer", (SCREEN_WIDTH // 2, 400), (240, 70), resume_game)
    pause_menu.add_button("Quitter", (SCREEN_WIDTH // 2, 500), (240, 70), ask_quit)

    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_GAME:
                        set_state(STATE_PAUSE)
                    elif state == STATE_PAUSE:
                        set_state(STATE_GAME)
                    elif state == STATE_DIFFICULTY:  # Nouveau : ESC pour revenir du menu difficulté
                        set_state(STATE_MENU)

        # Gestion des états
        if state == STATE_CINEMATIC:
            screen.blit(cinematic_images[cinematic_index], (0, 0))
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    cinematic_index += 1
                    if cinematic_index >= len(cinematic_images):
                        set_state(STATE_GAME)

        elif state == STATE_MENU:
            main_menu.handle_events(events)
            main_menu.draw()

        elif state == STATE_DIFFICULTY:  # Nouvel état
            difficulty_menu.handle_events(events)
            difficulty_menu.draw()

        elif state == STATE_GAME:
            game.handle_events()
            game.update()
            game.draw()

        elif state == STATE_PAUSE:
            pause_menu.handle_events(events)
            pause_menu.draw()

        elif state == STATE_CREDITS:
            credits_screen.handle_events(events)
            credits_screen.draw()

        elif state == STATE_QUIT and quit_popup:
            quit_popup.handle_events(events)
            quit_popup.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()