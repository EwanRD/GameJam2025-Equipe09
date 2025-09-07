from enum import Enum
import math

# Énumération pour les niveaux de difficulté
class DIFFICULTY_LEVEL(Enum):
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"

# Variable globale pour le niveau de difficulté actuel
CURRENT_DIFFICULTY = DIFFICULTY_LEVEL.NORMAL

# Paramètres globaux
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900
FPS = 60
TOTAL_TIME = 10
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
        }
    }
    return stats[difficulty]

# Statistiques de la liche basées sur la difficulté
def get_lich_stats(difficulty):
    """Retourne les statistiques de la liche en fonction de la difficulté"""
    stats = {
        DIFFICULTY_LEVEL.EASY: {
            "health": 25,
            "velocity": 3,
            "cooldown": 1.2
        },
        DIFFICULTY_LEVEL.NORMAL: {
            "health": 50,
            "velocity": 4,
            "cooldown": 1
        },
        DIFFICULTY_LEVEL.HARD: {
            "health": 50,
            "velocity": 4,
            "cooldown": 0.85
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

# Fonction pour obtenir les statistiques actuelles de la liche
def get_current_lich_stats():
    """Retourne les statistiques de la liche pour la difficulté actuelle"""
    return get_lich_stats(CURRENT_DIFFICULTY)

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

#Fireball
FIREBALL_SPEED = 3
FIREBALL_DIAG_SPEED = FIREBALL_SPEED/math.sqrt(2)

#Magic Missile
MAGIC_SPEED = 3
MAGIC_DIAG_SPEED = MAGIC_SPEED/math.sqrt(2)

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