import os
import pygame
from settings import MUSIC_FILE

def start_music():
   if not os.path.exists(MUSIC_FILE):
       return

   try:
       pygame.mixer.init()
       pygame.mixer.music.load(MUSIC_FILE)
       pygame.mixer.music.set_volume(0.45)
       pygame.mixer.music.play(-1)
   except pygame.error:
       pass
