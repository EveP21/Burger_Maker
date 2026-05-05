import os
import pygame
from settings import SPRITE_FOLDER, INGREDIENT_DATA, TOP_BUN, BOTTOM_BUN_SPRITE, BACKGROUND_SPRITE

def load_image(path):
   if not os.path.exists(path):
       return None

   try:
       return pygame.image.load(path).convert_alpha()
   except pygame.error:
       return None

def load_assets():
   assets = {}

   assets["background"] = load_image(os.path.join(SPRITE_FOLDER, BACKGROUND_SPRITE))
   assets["bottom_bun"] = load_image(os.path.join(SPRITE_FOLDER, BOTTOM_BUN_SPRITE))
   assets["top_bun"] = load_image(os.path.join(SPRITE_FOLDER, TOP_BUN["sprite"]))

   for name, data in INGREDIENT_DATA.items():
       assets[name] = load_image(os.path.join(SPRITE_FOLDER, data["sprite"]))

   return assets
