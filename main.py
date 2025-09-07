import pygame
import sys
import time
import sprites
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FPS, DIFFICULTY_LEVEL, set_difficulty
from menu import Menu, QuitPopup
from credits import Credits
from game import Game
from difficulty import Difficulty
from tutoriel import Tutoriel

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TOMB BOUND")
    
    sprites.load_sprites()

    # Cinématique
    cinematic_index = 0
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
    STATE_INFINITE_GAME_OVER = "infinite_game_over"
    STATE_CINEMATIC = "cinematic"
    STATE_GAME = "game"
    STATE_PAUSE = "pause"
    STATE_CREDITS = "credits"
    STATE_QUIT = "quit_popup"
    state = STATE_MENU

    # Jeu
    game = Game()
    final_score = 0  # Pour stocker le score final en mode infini

    # Menus
    main_menu = Menu(screen, " ", sprites.TITLE_FONT, sprites.BUTTON_FONT, COLORS, sprites.BACKGROUND_IMAGE)
    pause_menu = Menu(screen, "Pause", sprites.TITLE_FONT, sprites.BUTTON_FONT, COLORS, None, with_overlay=True)
    quit_popup = None

    # Credits
    credits_screen = Credits(screen, sprites.TITLE_FONT, sprites.BUTTON_FONT, COLORS, lambda: set_state(STATE_MENU), sprites.CREDIT_BACKGROUND)

    # Tutoriel
    def on_tutorial_complete():
        nonlocal tutorial_played
        tutorial_played = True
        start_game()

    tutoriel = Tutoriel(screen, sprites.TITLE_FONT, sprites.BUTTON_FONT, COLORS, sprites.BACKGROUND_IMAGE, on_tutorial_complete)

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

    difficulty = Difficulty(screen, sprites.TITLE_FONT, sprites.BUTTON_FONT, COLORS, sprites.BACKGROUND_IMAGE, on_difficulty_selected)

    # Fonctions pour changer d'état
    def set_state(new_state):
        nonlocal state, cinematic_index
        old_state = state
        state = new_state
        if new_state == STATE_CINEMATIC:
            cinematic_index = 0
        if new_state == STATE_CREDITS:
            credits_screen.reset()

        if new_state == STATE_GAME and old_state == STATE_MENU:
            game.__init__()

    def start_game():
        nonlocal cinematic_played, game
        game = Game()    
        if not cinematic_played:
            cinematic_played = True
            set_state(STATE_CINEMATIC)
        else:
            set_state(STATE_GAME)

    def show_difficulty():
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
        quit_popup = QuitPopup(screen, sprites.BUTTON_FONT, COLORS, origin, on_yes, on_no)
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
        surf = sprites.BUTTON_FONT.render(text, True, (255, 255, 255))
        surf_rect = surf.get_rect(center=center)
        screen.blit(surf, surf_rect)

        # Retourne True si cliqué
        clicked = pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos)
        if clicked:
            callback()
        return rect

    def draw_infinite_game_over():
        """Dessine l'écran de game over spécifique au mode infini"""
        # Fond semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Titre "GAME OVER"
        title_font = pygame.font.SysFont("Arial", 72, bold=True)
        title_text = title_font.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_text, title_rect)

        # Statistiques
        stats_font = pygame.font.SysFont("Arial", 36)
        
        # Score final
        score_text = stats_font.render(f"Score Final: {final_score}", True, (255, 215, 0))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(score_text, score_rect)
        
        # Vague atteinte
        wave_text = stats_font.render(f"Vague Atteinte: {game.wave}", True, (255, 255, 255))
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(wave_text, wave_rect)
        
        # Ennemis tués
        kills_text = stats_font.render(f"Ennemis Éliminés: {game.enemies_killed}", True, (255, 255, 255))
        kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        screen.blit(kills_text, kills_rect)
        
        # Temps survécu
        time_survived = int(time.time() - game.start_time)
        minutes = time_survived // 60
        seconds = time_survived % 60
        time_text = stats_font.render(f"Temps Survécu: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(time_text, time_rect)

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
            screen.blit(sprites.CINEMATIC_IMAGES[cinematic_index], (0, 0))
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    cinematic_index += 1
                    if cinematic_index >= len(sprites.CINEMATIC_IMAGES):
                        set_state(STATE_GAME)

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
                if game.is_infinite:
                    # En mode infini, calculer le score final
                    final_score = game.get_final_score()
                    set_state(STATE_INFINITE_GAME_OVER)
                else:
                    set_state(STATE_GAME_OVER)
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

        elif state == STATE_INFINITE_GAME_OVER:
            draw_infinite_game_over()
            # Boutons avec couleurs spéciales
            gold_colors = ((200, 150, 50), (255, 215, 0))  # Or pour rejouer
            silver_colors = ((100, 100, 100), (180, 180, 180))  # Argent pour menu
            
            draw_button("Rejouer", (SCREEN_WIDTH//4, SCREEN_HEIGHT - 80), 200, 60, mouse_pos,
                        lambda: (game.__init__(), set_state(STATE_GAME)), gold_colors)
            draw_button("Menu", (3*SCREEN_WIDTH//4, SCREEN_HEIGHT - 80), 200, 60, mouse_pos,
                        lambda: (game.__init__(), set_state(STATE_MENU)), silver_colors)

        elif state == STATE_QUIT and quit_popup:
            quit_popup.handle_events(events)
            quit_popup.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()