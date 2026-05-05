import pygame
# Main Variables

score = 0 # determinará la puntuación del jugador
ingredients = 0 # determinará los ingredientes que tiene la hamburguesa (para poner un máximo de ingredientes por hambugruesa)
lives = 3 # la cantidad de vidas

# 16:9 canvas
WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("16:9 Game Canvas")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # Background color

    pygame.display.flip()

pygame.quit()