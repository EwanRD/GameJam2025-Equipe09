import pygame

def play_sound(sound_path, volume=1.0):
    sound = pygame.mixer.Sound(sound_path)
    sound.set_volume(volume)
    sound.play()