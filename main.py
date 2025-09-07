import pygame
import sys
import time
import media

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FPS, DIFFICULTY_LEVEL, set_difficulty
from menu import Menu, QuitPopup
from credits import Credits
from game import Game
from difficulty import Difficulty
from tutoriel import Tutoriel

def play_menu_music():
    """Joue la musique du menu"""
    pygame.mixer.music.load(media.MENU_MUSIC)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

def play_game_music():
    """Joue la musique de jeu"""
    pygame.mixer.music.load(media.GAME_MUSIC)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

def play_boss_music():
    """Joue la musique du boss"""
    pygame.mixer.music.load(media.BOSS_MUSIC)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TOMB BOUND")

    media.load_sprites()

    play_menu_music()

    # Cinématique
    cinematic_index = 0
    endcinematic_index = 0
    cinematic_played = False
    tutorial_played = False

    # Game Over image
    game_over_img = pygame.image.load("assets/images/Game_Over.png")
    game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # États
    STATE_DIFFICULTY = "difficulty"
    STATE_TUTORIAL = "tutorial"
    STATE_MENU = "menu"
    STATE_GAME_OVER = "game_over"
    STATE_CINEMATIC = "cinematic"
    STATE_END_CINEMATIC = "end_cinematic"
    STATE_GAME = "game"
    STATE_PAUSE = "pause"
    STATE_CREDITS = "credits"
    STATE_QUIT = "quit_popup"
    state = STATE_MENU

    # Jeu
    game = Game()

    # Menus
    main_menu = Menu(screen, " ", media.TITLE_FONT, media.BUTTON_FONT, COLORS, media.BACKGROUND_IMAGE)
    pause_menu = Menu(screen, "Pause", media.TITLE_FONT, media.BUTTON_FONT, COLORS, None, with_overlay=True)
    quit_popup = None

    # Credits
    credits_screen = Credits(screen, media.TITLE_FONT, media.BUTTON_FONT, COLORS, lambda: set_state(STATE_MENU), media.CREDIT_BACKGROUND)

    # Tutoriel
    def on_tutorial_complete():
        nonlocal tutorial_played
        tutorial_played = True
        start_game()

    tutoriel = Tutoriel(screen, media.TITLE_FONT, media.BUTTON_FONT, COLORS, media.BACKGROUND_IMAGE, on_tutorial_complete)

    # Menu de difficulté (modifié pour inclure le mode infini)
    def on_difficulty_selected(difficulty):
        nonlocal tutorial_played
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
            elif difficulty == 'infinite':
                set_difficulty(DIFFICULTY_LEVEL.INFINITE)

            # En mode infini, pas besoin de tutoriel (ou l'afficher quand même si souhaité)
            if not tutorial_played and difficulty != 'infinite':
                set_state(STATE_TUTORIAL)
            else:
                start_game()

    difficulty = Difficulty(screen, media.TITLE_FONT, media.BUTTON_FONT, COLORS, media.BACKGROUND_IMAGE, on_difficulty_selected)

    # Fonctions pour changer d'état
    def set_state(new_state):
        nonlocal state, cinematic_index, endcinematic_index
        old_state = state
        state = new_state
        if new_state == STATE_CINEMATIC:
            cinematic_index = 0
        if new_state == STATE_END_CINEMATIC:
            endcinematic_index = 0
        if new_state == STATE_CREDITS:
            credits_screen.reset()
        if new_state == STATE_GAME and old_state == STATE_MENU:
            game.__init__()

    def start_game():
        nonlocal cinematic_played, game
        game = Game()
        play_game_music()
        if not cinematic_played:
            cinematic_played = True
            set_state(STATE_CINEMATIC)
        else:
            set_state(STATE_GAME)

    def show_difficulty():
        set_state(STATE_DIFFICULTY)

    def show_credits():
        play_menu_music()
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
        quit_popup = QuitPopup(screen, media.BUTTON_FONT, COLORS, origin, on_yes, on_no)
        state = STATE_QUIT

    # Ajouter boutons
    main_menu.add_button("Jouer", (SCREEN_WIDTH // 2, 400), (240, 70), show_difficulty)  
    main_menu.add_button("Crédits", (SCREEN_WIDTH // 2, 500), (240, 70), show_credits)
    main_menu.add_button("Quitter", (SCREEN_WIDTH // 2, 600), (240, 70), ask_quit)

    # Ajouter boutons pause
    pause_menu.add_button("Continuer", (SCREEN_WIDTH // 2, 400), (240, 70), resume_game)
    pause_menu.add_button("Quitter", (SCREEN_WIDTH // 2, 500), (240, 70), ask_quit)

    clock = pygame.time.Clock()
    running = True

    # Fonction pour dessiner un bouton stylisé avec hover
    def draw_button(text, center, width, height, mouse_pos, callback, color=None):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = center

        # Couleur de fond
        if color:
            base_color, hover_color = color
        else:
            base_color = (50, 50, 50)
            hover_color = (100, 100, 100)
        
        button_color = hover_color if rect.collidepoint(mouse_pos) else base_color
        pygame.draw.rect(screen, button_color, rect, border_radius=15)

        # Texte
        surf = media.BUTTON_FONT.render(text, True, (255, 255, 255))
        surf_rect = surf.get_rect(center=center)
        screen.blit(surf, surf_rect)

        # Retourne True si cliqué
        clicked = pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos)
        if clicked:
            callback()
        return rect

    while running:
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_GAME:
                        set_state(STATE_PAUSE)
                    elif state == STATE_PAUSE:
                        set_state(STATE_GAME)
                    elif state == STATE_DIFFICULTY:
                        set_state(STATE_MENU)
                    elif state == STATE_TUTORIAL:
                        tutoriel.skip_tutorial()

        # Gestion des états
        if state == STATE_CINEMATIC:
            screen.blit(media.CINEMATIC_IMAGES[cinematic_index], (0, 0))
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    cinematic_index += 1
                    if cinematic_index >= len(media.CINEMATIC_IMAGES):
                        set_state(STATE_GAME)
        elif state == STATE_END_CINEMATIC:
            screen.blit(media.ENDCINEMATIC_IMAGES[endcinematic_index], (0, 0))
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    endcinematic_index += 1
                    if endcinematic_index >= len(media.ENDCINEMATIC_IMAGES):
                        # Reset des variables pour une nouvelle partie
                        cinematic_played = False
                        tutorial_played = False
                        play_menu_music()
                        set_state(STATE_MENU)

        elif state == STATE_MENU:
            main_menu.handle_events(events)
            main_menu.draw()

        elif state == STATE_DIFFICULTY:
            difficulty.handle_events(events)
            difficulty.draw()

        elif state == STATE_TUTORIAL: 
            tutoriel.handle_events(events)
            tutoriel.draw()

        elif state == STATE_GAME:
            game.handle_events()
            result = game.update()
            if result == "game_over":
                set_state(STATE_GAME_OVER)
            elif result == "boss_defeated":
                set_state(STATE_END_CINEMATIC)
            elif result == "boss_spawned":
                play_boss_music()
            game.draw()

        elif state == STATE_PAUSE:
            pause_menu.handle_events(events)
            pause_menu.draw()

        elif state == STATE_CREDITS:
            credits_screen.handle_events(events)
            credits_screen.draw()

        elif state == STATE_GAME_OVER:
            screen.blit(game_over_img, (0, 0))
            draw_button("Rejouer", (SCREEN_WIDTH//4, SCREEN_HEIGHT - 80), 200, 60, mouse_pos,
                        lambda: (game.__init__(), set_state(STATE_GAME)))
            draw_button("Menu", (3*SCREEN_WIDTH//4, SCREEN_HEIGHT - 80), 200, 60, mouse_pos,
                        lambda: (game.__init__(), set_state(STATE_MENU)))

        elif state == STATE_QUIT and quit_popup:
            quit_popup.handle_events(events)
            quit_popup.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()