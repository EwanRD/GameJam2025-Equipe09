import pygame

# sprites
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

SKELETIN_SPRITES =  {
            "down": [
                pygame.image.load("assets/sprites/Enemies/Squelette/devant.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/devantmarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/devantmarche2.png").convert_alpha(),
            ],
            "up": [
                pygame.image.load("assets/sprites/Enemies/Squelette/derriere.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/derrieremarche1.png").convert_alpha(),
                pygame.image.load("assets/sprites/Enemies/Squelette/derrieremarche2.png").convert_alpha(),
            ],            "left": [
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
            ],            "left": [
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
            ],            "left": [
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
# image
MAP = pygame.image.load("assets/mapgamejam.png").convert()
HEART_FULL = pygame.image.load("assets/sprites/UI/Heart/coeurplein.png").convert_alpha()
HEART_EMPTY = pygame.image.load("assets/sprites/UI/Heart/coeurvide.png").convert_alpha()

## son

# music
BACKGROUND_MUSIC = "assets/sounds/crypt_loop.wav"

# sound effect
HURT_SOUND = pygame.mixer.Sound("assets/sounds/hurt.mp3")
GAMEOVER_SOUND = pygame.mixer.Sound("assets/sounds/GameOver.wav")
ORC_DEATH = pygame.mixer.Sound("assets/sounds/orc_death.mp3")
SHOOT_SOUND = pygame.mixer.Sound("assets/sounds/shoot.ogg")
DEATH_SOUND = pygame.mixer.Sound("assets/sounds/skeleton_death.mp3")
HIT_SOUND = pygame.mixer.Sound("assets/sounds/hurt.mp3")