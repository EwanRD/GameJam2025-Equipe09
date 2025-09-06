import math
import settings  # pour FIREBALL_SPEED

def play_sound(sound, volume=1.0):
    """Play a pygame sound with a given volume"""
    sound.set_volume(volume)
    sound.play()

def get_direction_vector(src_x, src_y, dst_x, dst_y, speed):
    """Return a normalized direction vector scaled by speed"""
    dx = dst_x - src_x
    dy = dst_y - src_y
    distance = math.hypot(dx, dy)
    if distance == 0:
        return 0, 0
    return speed * dx / distance, speed * dy / distance
