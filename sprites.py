import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Déclarations vides (seront remplies par load_sprites)
PLAYER_SPRITES = {}
SKELETON_SPRITES = {}
ORC_SPRITES = {}
GHOST_SPRITES = {}
BOSS_SPRITES = {}
CINEMATIC_IMAGES = []
FIREBALL_SPRITE = None

MAP = None
HEART_FULL = None
HEART_EMPTY = None

# Sons (chargés directement, pas besoin de display.init pour ça)
BACKGROUND_MUSIC = "assets/sounds/crypt_loop.wav"
BOSS_MUSIC = "assets/sounds/BossMusic.mp3"
BACKGROUND_IMAGE = None
CREDIT_BACKGROUND = None

HURT_SOUND = None
GAMEOVER_SOUND = None
ORC_DEATH = None
SHOOT_SOUND = None
DEATH_SOUND = None
HIT_SOUND = None
FIREBALL_HIT_SOUND = None
FIREBALL_SOUND = None
MAGIC_SOUND = None
PLAYER_POWER_SOUND = None
LICH_TP_SOUND = None

TITLE_FONT = None
BUTTON_FONT = None

def load_sprites():
    global PLAYER_SPRITES, SKELETON_SPRITES, ORC_SPRITES, GHOST_SPRITES, BOSS_SPRITES,\
        CINEMATIC_IMAGES, FIREBALL_SPRITE, BACKGROUND_IMAGE, CREDIT_BACKGROUND
    global MAP, HEART_FULL, HEART_EMPTY
    global HURT_SOUND, GAMEOVER_SOUND, ORC_DEATH, SHOOT_SOUND, DEATH_SOUND, HIT_SOUND, FIREBALL_SOUND, FIREBALL_HIT_SOUND, MAGIC_SOUND, \
        PLAYER_POWER_SOUND, LICH_TP_SOUND
    global TITLE_FONT, BUTTON_FONT

    # --- Joueur ---
    PLAYER_SPRITES = {
        "down": [
            pygame.image.load("assets/sprites/Player/devant.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/devantmarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/devantmarche2.png").convert_alpha(),
        ],
        "up": [
            pygame.image.load("assets/sprites/Player/derriere.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/derrieremarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/derrieremarche2.png").convert_alpha(),
        ],
        "left": [
            pygame.image.load("assets/sprites/Player/gauche.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/gauchemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/gauchemarche2.png").convert_alpha(),
        ],
        "right": [
            pygame.image.load("assets/sprites/Player/droite.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/droitemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Player/droitemarche2.png").convert_alpha(),
        ],
    }

    # --- Squelette ---
    SKELETON_SPRITES = {
        "down": [
            pygame.image.load("assets/sprites/Enemies/Squelette/devant.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/devantmarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/devantmarche2.png").convert_alpha(),
        ],
        "up": [
            pygame.image.load("assets/sprites/Enemies/Squelette/derriere.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/derrieremarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/derrieremarche2.png").convert_alpha(),
        ],
        "left": [
            pygame.image.load("assets/sprites/Enemies/Squelette/gauche.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/gauchemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/gauchemarche2.png").convert_alpha(),
        ],
        "right": [
            pygame.image.load("assets/sprites/Enemies/Squelette/droite.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/droitemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Squelette/droitemarche2.png").convert_alpha(),
        ],
    }

    # --- Orc ---
    ORC_SPRITES = {
        "down": [
            pygame.image.load("assets/sprites/Enemies/Orc/devant.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/devantmarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/devantmarche2.png").convert_alpha(),
        ],
        "up": [
            pygame.image.load("assets/sprites/Enemies/Orc/derriere.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/derrieremarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/derrieremarche2.png").convert_alpha(),
        ],
        "left": [
            pygame.image.load("assets/sprites/Enemies/Orc/gauche.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/gauchemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/gauchemarche2.png").convert_alpha(),
        ],
        "right": [
            pygame.image.load("assets/sprites/Enemies/Orc/droite.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/droitemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Orc/droitemarche2.png").convert_alpha(),
        ],
    }

    # --- Ghost ---
    GHOST_SPRITES = {
        "down": [
            pygame.image.load("assets/sprites/Enemies/Ghost/devant.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/devantmarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/devantmarche2.png").convert_alpha(),
        ],
        "up": [
            pygame.image.load("assets/sprites/Enemies/Ghost/derriere.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/derrieremarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/derrieremarche2.png").convert_alpha(),
        ],
        "left": [
            pygame.image.load("assets/sprites/Enemies/Ghost/gauche.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/gauchemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/gauchemarche2.png").convert_alpha(),
        ],
        "right": [
            pygame.image.load("assets/sprites/Enemies/Ghost/droite.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/droitemarche1.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Ghost/droitemarche2.png").convert_alpha(),
        ],
    }

    # --- Boss ---
    BOSS_SPRITES = [
            pygame.image.load("assets/sprites/Enemies/Liche/devant.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Liche/devantmarche2.png").convert_alpha(),
            pygame.image.load("assets/sprites/Enemies/Liche/devantmarche1.png").convert_alpha(),
        ]

    CINEMATIC_IMAGES =  [
        pygame.transform.scale(pygame.image.load("assets/images/cinematique1.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(pygame.image.load("assets/images/cinematique2.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        pygame.transform.scale(pygame.image.load("assets/images/cinematique3.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    ]

    FIREBALL_SPRITE = pygame.image.load("assets/sprites/Projectiles/Ghost_burst/ghost_burst.png").convert_alpha()

    BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/screen.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    CREDIT_BACKGROUND = pygame.transform.scale(pygame.image.load("assets/images/credits.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    # --- Images UI ---
    MAP = pygame.image.load("assets/mapgamejam.png").convert()
    HEART_FULL = pygame.image.load("assets/sprites/UI/Heart/coeurplein.png").convert_alpha()
    HEART_EMPTY = pygame.image.load("assets/sprites/UI/Heart/coeurvide.png").convert_alpha()

    # --- Sons ---
    HURT_SOUND = pygame.mixer.Sound("assets/sounds/hurt.mp3")
    GAMEOVER_SOUND = pygame.mixer.Sound("assets/sounds/GameOver.wav")
    ORC_DEATH = pygame.mixer.Sound("assets/sounds/orc_death.mp3")
    SHOOT_SOUND = pygame.mixer.Sound("assets/sounds/shoot.ogg")
    DEATH_SOUND = pygame.mixer.Sound("assets/sounds/skeleton_death.mp3")
    HIT_SOUND = pygame.mixer.Sound("assets/sounds/hurt.mp3")
    FIREBALL_SOUND = pygame.mixer.Sound("assets/sounds/shoot.ogg")
    FIREBALL_HIT_SOUND = pygame.mixer.Sound("assets/sounds/hurt.mp3")
    MAGIC_SOUND = pygame.mixer.Sound("assets/sounds/Lich_fireball.mp3")
    PLAYER_POWER_SOUND = pygame.mixer.Sound("assets/sounds/player_power.mp3")
    LICH_TP_SOUND = pygame.mixer.Sound("assets/sounds/Lich_tp.mp3")

    # -- Font --
    TITLE_FONT = pygame.font.Font("assets/the_centurion/The Centurion .ttf", 78)
    BUTTON_FONT = pygame.font.SysFont("Arial", 32)
