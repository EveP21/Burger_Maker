import pygame
from settings import *

score = START_SCORE
ingredients = START_INGREDIENTS
lives = START_LIVES

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

running = True
clock = pygame.time.Clock()

while running:
   clock.tick(FPS)

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

   screen.fill((35, 35, 35))
   pygame.display.flip()

pygame.quit()

