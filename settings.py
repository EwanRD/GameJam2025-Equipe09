
from enum import Enum
import math

# Paramètres globaux
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900
FPS = 60
TOTAL_TIME = 300

COLORS = {
    "black": (0, 0, 0),
    "brown": (139, 69, 19),
    "white": (240, 240, 240),
    "button": (60, 60, 80),
    "hover": (100, 100, 160),
    "overlay": (0, 0, 0)  # pour les menus avec overlay, alpha moins noir
}

# map
SPAWN_ZONE =  [(682,15), (1242,420), (562,855), (6, 419)]
LEFT_WALL = []

## Attributes for all entity

# Entity attributes

# player attributes
PLAYER_SPEED = 5
PLAYER_HEALTH = 3
PLAYER_DOMMAGE = 1
PLAYER_COULDOWN = 0.5

## enemy

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
    H  = "assets/sprites/Projectiles/Arrow/flechehaut.png"          # Haut
    B  = "assets/sprites/Projectiles/Arrow/flechebas.png"           # Bas
    G  = "assets/sprites/Projectiles/Arrow/flechegauche.png"        # Gauche
    D  = "assets/sprites/Projectiles/Arrow/flechedroite.png"        # Droite
    HG = "assets/sprites/Projectiles/Arrow/flechehautgauche.png"    # Haut-Gauche
    HD = "assets/sprites/Projectiles/Arrow/flechehautdroite.png"    # Haut-Droite
    BG =  "assets/sprites/Projectiles/Arrow/flechebasgauche.png"    # Bas-Gauche
    BD = "assets/sprites/Projectiles/Arrow/flechebasdroite.png"     # Bas-Droite

#Fireball
FIREBALL_SPEED = 3
FIREBALL_DIAG_SPEED = FIREBALL_SPEED/math.sqrt(2)

class DIRECTION(Enum):
    H  = (0, -ARROW_SPEED)             # Haut
    B  = (0, ARROW_SPEED)              # Bas
    G  = (-ARROW_SPEED, 0)             # Gauche
    D  = (ARROW_SPEED, 0)              # Droite
    HG = (-ARROW_SPEED, -ARROW_SPEED)  # Haut-Gauche
    HD = (ARROW_SPEED, -ARROW_SPEED)   # Haut-Droite
    BG = (-ARROW_SPEED, ARROW_SPEED)   # Bas-Gauche
    BD = (ARROW_SPEED, ARROW_SPEED)    # Bas-Droite

# wave
FIRST_WAVE =1
WAVE_INTERVAL = 10
ENEMY_COUNT = 3
MAX_ENEMY_COUNT = 8

