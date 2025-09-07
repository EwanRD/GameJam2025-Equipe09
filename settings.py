from enum import Enum
import math

# Énumération pour les niveaux de difficulté
class DIFFICULTY_LEVEL(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    INFINITE = "infinite"  # Nouveau mode infini

# Variable globale pour le niveau de difficulté actuel
CURRENT_DIFFICULTY = DIFFICULTY_LEVEL.NORMAL

# Paramètres globaux
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900
FPS = 60

COLORS = {
    "black": (0, 0, 0),
    "brown": (139, 69, 19),
    "white": (240, 240, 240),
    "button": (60, 60, 80),
    "hover": (100, 100, 160),
    "overlay": (0, 0, 0, 100) # pour les menus avec overlay, alpha moins noir
}

# map
SPAWN_ZONE = [(682,15), (1242,420), (562,855), (6, 419)]
LEFT_WALL = []

## Attributes for all entity
# Entity attributes
# player attributes
PLAYER_SPEED = 5

# Statistiques du joueur basées sur la difficulté
def get_player_stats(difficulty):
    """Retourne les statistiques du joueur en fonction de la difficulté"""
    stats = {
        DIFFICULTY_LEVEL.EASY: {
            "health": 3,
            "damage": 2,
            "cooldown": 0.5
        },
        DIFFICULTY_LEVEL.NORMAL: {
            "health": 3,
            "damage": 1,
            "cooldown": 0.5
        },
        DIFFICULTY_LEVEL.HARD: {
            "health": 1,
            "damage": 1,
            "cooldown": 0.5
        },
        DIFFICULTY_LEVEL.INFINITE: {
            "health": 3,
            "damage": 1,
            "cooldown": 0.5
        }
    }
    return stats[difficulty]

# Fonction pour définir la difficulté
def set_difficulty(difficulty):
    """Définit le niveau de difficulté actuel"""
    global CURRENT_DIFFICULTY
    CURRENT_DIFFICULTY = difficulty

# Fonction pour obtenir les statistiques actuelles du joueur
def get_current_player_stats():
    """Retourne les statistiques du joueur pour la difficulté actuelle"""
    return get_player_stats(CURRENT_DIFFICULTY)

# Valeurs par défaut (peuvent être remplacées par get_current_player_stats())
PLAYER_HEALTH = 3
PLAYER_DOMMAGE = 1
PLAYER_COULDOWN = 0.5

# enemy
#skeleton
SKELETON_HEALTH = 2
# orc
ORC_HEALTH = 3
# ghost
GHOST_HEALTH = 1
GHOST_COULDOWN = 1.5

## Attribut globale des projectiles
# Arrow
ARROW_SPEED = 5
ARROW_DIAG_SPEED = ARROW_SPEED / math.sqrt(2)

# la liste des différent affichage d'une flèche
class ARROW_DIRECTION(Enum):
    H = "assets/sprites/Projectiles/Arrow/flechehaut.png" # Haut
    B = "assets/sprites/Projectiles/Arrow/flechebas.png" # Bas
    G = "assets/sprites/Projectiles/Arrow/flechegauche.png" # Gauche
    D = "assets/sprites/Projectiles/Arrow/flechedroite.png" # Droite
    HG = "assets/sprites/Projectiles/Arrow/flechehautgauche.png" # Haut-Gauche
    HD = "assets/sprites/Projectiles/Arrow/flechehautdroite.png" # Haut-Droite
    BG = "assets/sprites/Projectiles/Arrow/flechebasgauche.png" # Bas-Gauche
    BD = "assets/sprites/Projectiles/Arrow/flechebasdroite.png" # Bas-Droite

class GOLDARROW_DIRECTION(Enum):
    H = "assets/sprites/Projectiles/Arrow/flecheorhaut.png" # Haut
    B = "assets/sprites/Projectiles/Arrow/flecheorbas.png" # Bas
    G = "assets/sprites/Projectiles/Arrow/flecheorgauche.png" # Gauche
    D = "assets/sprites/Projectiles/Arrow/flecheordroite.png" # Droite
    HG = "assets/sprites/Projectiles/Arrow/flecheorhautgauche.png" # Haut-Gauche
    HD = "assets/sprites/Projectiles/Arrow/flecheorhautdroite.png" # Haut-Droite
    BG = "assets/sprites/Projectiles/Arrow/flecheorbasgauche.png" # Bas-Gauche
    BD = "assets/sprites/Projectiles/Arrow/flecheorbasdroite.png" # Bas-Droite

#Fireball
FIREBALL_SPEED = 3
FIREBALL_DIAG_SPEED = FIREBALL_SPEED/math.sqrt(2)

class DIRECTION(Enum):
    H = (0, -ARROW_SPEED) # Haut
    B = (0, ARROW_SPEED) # Bas
    G = (-ARROW_SPEED, 0) # Gauche
    D = (ARROW_SPEED, 0) # Droite
    HG = (-ARROW_SPEED, -ARROW_SPEED) # Haut-Gauche
    HD = (ARROW_SPEED, -ARROW_SPEED) # Haut-Droite
    BG = (-ARROW_SPEED, ARROW_SPEED) # Bas-Gauche
    BD = (ARROW_SPEED, ARROW_SPEED) # Bas-Droite

# wave
FIRST_WAVE = 1
WAVE_INTERVAL = 10
ENEMY_COUNT = 3
MAX_ENEMY_COUNT = 8

def get_total_time(difficulty):
    """Retourne le temps total du jeu en fonction de la difficulté"""
    times = {
        DIFFICULTY_LEVEL.EASY: 180, # 3 minutes
        DIFFICULTY_LEVEL.NORMAL: 300, # 5 minutes
        DIFFICULTY_LEVEL.HARD: 300, # 5 minutes
        DIFFICULTY_LEVEL.INFINITE: -1 # Temps infini (-1 indique pas de limite)
    }
    return times[difficulty]

def get_current_total_time():
    """Retourne le temps total pour la difficulté actuelle"""
    return get_total_time(CURRENT_DIFFICULTY)

def is_infinite_mode():
    """Vérifie si le mode actuel est le mode infini"""
    return CURRENT_DIFFICULTY == DIFFICULTY_LEVEL.INFINITE