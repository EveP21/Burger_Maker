import os
import pygame
from settings import MUSIC_FILE


def start_music():
    music_file = os.fspath(MUSIC_FILE)
    if not os.path.exists(music_file) or os.path.getsize(music_file) <= 2:
        return

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
    except pygame.error:
        # El juego no debe romperse si la PC no tiene audio disponible.
        pass
