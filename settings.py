
from enum import Enum
import math

# Paramètres globaux
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 900
FPS = 60

COLORS = {
    "brown": (139, 69, 19),
    "white": (240, 240, 240),
    "button": (60, 60, 80),
    "hover": (100, 100, 160),
    "overlay": (0, 0, 0)  # pour les menus avec overlay, alpha moins noir
}

# player attributes
PLAYER_SPEED = 5
PLAYER_HEALTH = 3
PLAYER_DOMMAGE = 1
PLAYER_COULDOWN = 0.5

# Vitesse globale des projectiles
PROJ_SPEED = 5
PROJ_DIAG_SPEED = PROJ_SPEED / math.sqrt(2)

class DIRECTION(Enum):
    H  = (0, -PROJ_SPEED)        # Haut
    B  = (0, PROJ_SPEED)         # Bas
    G  = (-PROJ_SPEED, 0)        # Gauche
    D  = (PROJ_SPEED, 0)         # Droite
    HG = (-PROJ_DIAG_SPEED, -PROJ_DIAG_SPEED)  # Haut-Gauche
    HD = (PROJ_DIAG_SPEED, -PROJ_DIAG_SPEED)   # Haut-Droite
    BG = (-PROJ_DIAG_SPEED, PROJ_DIAG_SPEED)   # Bas-Gauche
    BD = (PROJ_DIAG_SPEED, PROJ_DIAG_SPEED)    # Bas-Droite

class ARROW_DIRECTION(Enum):
    H  = "assets/sprites/Projectiles/Arrow/flechehaut.png"           # Haut
    B  = "assets/sprites/Projectiles/Arrow/flechebas.png"           # Bas
    G  = "assets/sprites/Projectiles/Arrow/flechegauche.png"        # Gauche
    D  = "assets/sprites/Projectiles/Arrow/flechedroite.png"        # Droite
    HG = "assets/sprites/Projectiles/Arrow/flechehautgauche.png"     # Haut-Gauche
    HD = "assets/sprites/Projectiles/Arrow/flechehautdroite.png"     # Haut-Droite
    BG =  "assets/sprites/Projectiles/Arrow/flechebasgauche.png"    # Bas-Gauche
    BD = "assets/sprites/Projectiles/Arrow/flechebasdroite.png"     # Bas-Droite


