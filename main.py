import random
import pygame

from settings import *
from assets import load_assets
from recipe import generate_recipe, collect_required, is_recipe_complete, INGREDIENT_TYPES

score = START_SCORE
ingredients = START_INGREDIENTS
lives = START_LIVES
level = 1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Arial", 46, bold=True)
font = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 22)

assets = load_assets()
# MUSIC_HOOK

paddle = pygame.Rect(
   WIDTH // 2 - PADDLE_WIDTH // 2,
   HEIGHT - 90,
   PADDLE_WIDTH,
   PADDLE_HEIGHT
)

falling_objects = []
spawn_timer = 0
current_recipe = generate_recipe(level)
round_start_ticks = pygame.time.get_ticks()
game_over = False

def get_speed():
   return BASE_FALL_SPEED + level * SPEED_PER_LEVEL

def get_spawn_delay():
   return max(MIN_SPAWN_DELAY, BASE_SPAWN_DELAY - level * 3)

def reset_round(next_level=False):
   global level, current_recipe, falling_objects, spawn_timer, round_start_ticks

   if next_level:
       level += 1

   current_recipe = generate_recipe(level)
   falling_objects = []
   spawn_timer = 0
   round_start_ticks = pygame.time.get_ticks()

def lose_life():
   global lives, game_over

   lives -= 1

   if lives <= 0:
       game_over = True
   else:
       reset_round(False)

def make_falling_object():
   recipe_done = is_recipe_complete(current_recipe)

   if recipe_done and random.random() < 0.35:
       kind = "top_bun"
       width = 100
       height = 50
   else:
       kind = random.choice(INGREDIENT_TYPES)
       width = 70
       height = 45

   return {
       "kind": kind,
       "rect": pygame.Rect(random.randint(20, WIDTH - width - 20), -height, width, height),
       "speed": get_speed() + random.uniform(0, 2)
   }

def draw_background():
   bg = assets.get("background")

   if bg:
       screen.blit(pygame.transform.scale(bg, (WIDTH, HEIGHT)), (0, 0))
   else:
       screen.fill((32, 38, 45))

def draw_sprite_or_shape(kind, rect):
   image = assets.get(kind)

   if image:
       screen.blit(pygame.transform.scale(image, (rect.width, rect.height)), rect)
       return

   if kind == "bottom_bun":
       pygame.draw.ellipse(screen, (230, 160, 80), rect)
       pygame.draw.rect(screen, (170, 95, 45), (rect.x, rect.y + rect.height // 2, rect.width, rect.height // 2), border_radius=12)
       return

   if kind == "top_bun":
       pygame.draw.ellipse(screen, TOP_BUN["color"], rect)
       for x in (rect.x + 25, rect.centerx, rect.right - 25):
           pygame.draw.circle(screen, (255, 245, 210), (x, rect.y + 15), 4)
       return

   color = INGREDIENT_DATA[kind]["color"]

   if kind == "queso":
       pygame.draw.polygon(screen, color, [
           (rect.left, rect.top + 5),
           (rect.right, rect.top),
           (rect.right - 10, rect.bottom),
           (rect.left + 10, rect.bottom)
       ])
   elif kind == "tomate":
       pygame.draw.ellipse(screen, color, rect)
   elif kind == "lechuga":
       pygame.draw.ellipse(screen, color, rect)
       pygame.draw.arc(screen, (30, 120, 40), rect, 0, 3.14, 3)
   elif kind == "tocino":
       pygame.draw.rect(screen, color, rect, border_radius=10)
       pygame.draw.line(screen, (240, 130, 120), (rect.left + 10, rect.centery), (rect.right - 10, rect.centery), 4)
   else:
       pygame.draw.rect(screen, color, rect, border_radius=12)

def draw_text(text, x, y, color=(255, 255, 255), small=False):
   selected_font = font_small if small else font
   surface = selected_font.render(text, True, color)
   screen.blit(surface, (x, y))

def draw_center(text, y, color=(255, 255, 255)):
   surface = font_big.render(text, True, color)
   screen.blit(surface, (WIDTH // 2 - surface.get_width() // 2, y))

def draw_hud():
   remaining_time = max(0, ROUND_TIME - (pygame.time.get_ticks() - round_start_ticks) // 1000)

   draw_text(f"Score: {score}", 30, 25)
   draw_text(f"Ingredientes: {ingredients}", 30, 60)
   draw_text(f"Vidas: {lives}", 30, 95)
   draw_text(f"Nivel: {level}", 30, 130)
   draw_text(f"Tiempo: {remaining_time}", 30, 165)

def draw_recipe_panel():
   panel = pygame.Rect(WIDTH - 390, 25, 350, 190)
   pygame.draw.rect(screen, (20, 20, 20), panel, border_radius=18)
   pygame.draw.rect(screen, (255, 255, 255), panel, 2, border_radius=18)

   draw_text("Orden actual", panel.x + 20, panel.y + 15)

   y = panel.y + 55
   for item in current_recipe["required"]:
       done = current_recipe["collected"][item] >= 1
       mark = "OK" if done else "--"
       draw_text(f"{mark} {item}", panel.x + 25, y, (210, 255, 210) if done else (255, 255, 255), small=True)
       y += 25

   if current_recipe["avoid"]:
       draw_text("Evita: " + ", ".join(current_recipe["avoid"]), panel.x + 25, panel.y + 155, (255, 120, 120), small=True)
   else:
       draw_text("Sin excluyentes", panel.x + 25, panel.y + 155, (200, 200, 200), small=True)

def handle_catch(kind):
   global score, ingredients

   if kind == "top_bun":
       if is_recipe_complete(current_recipe):
           score += TOP_BUN["points"] + level * 10
           reset_round(True)
       else:
           lose_life()
       return

   if kind in current_recipe["avoid"]:
       lose_life()
       return

   if kind not in current_recipe["required"]:
       lose_life()
       return

   if current_recipe["collected"][kind] == 0:
       score += INGREDIENT_DATA[kind]["points"]
       ingredients += 1
       collect_required(current_recipe, kind)
   else:
       lose_life()

running = True

while running:
   clock.tick(FPS)

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

       elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
           score = START_SCORE
           ingredients = START_INGREDIENTS
           lives = START_LIVES
           level = 1
           game_over = False
           reset_round(False)

       # PAUSE_EVENT_HOOK

   # PAUSE_LOOP_HOOK

   keys = pygame.key.get_pressed()

   if not game_over:
       if keys[pygame.K_LEFT] and paddle.left > 0:
           paddle.x -= PADDLE_SPEED

       if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
           paddle.x += PADDLE_SPEED

       spawn_timer += 1

       if spawn_timer >= get_spawn_delay():
           falling_objects.append(make_falling_object())
           spawn_timer = 0

       for obj in falling_objects[:]:
           obj["rect"].y += obj["speed"]

           if obj["rect"].colliderect(paddle):
               handle_catch(obj["kind"])

               if obj in falling_objects:
                   falling_objects.remove(obj)

           elif obj["rect"].top > HEIGHT:
               if obj in falling_objects:
                   falling_objects.remove(obj)
               lose_life()

       remaining_time = ROUND_TIME - (pygame.time.get_ticks() - round_start_ticks) // 1000

       if remaining_time <= 0:
           lose_life()

   draw_background()
   draw_sprite_or_shape("bottom_bun", paddle)

   for obj in falling_objects:
       draw_sprite_or_shape(obj["kind"], obj["rect"])

   draw_hud()
   draw_recipe_panel()

   if is_recipe_complete(current_recipe) and not game_over:
       draw_center("Ahora atrapa el pan de arriba", HEIGHT // 2 - 40, (255, 230, 120))

   if game_over:
       draw_center("GAME OVER", HEIGHT // 2 - 70, (255, 90, 90))
       draw_center("Presiona R para reiniciar", HEIGHT // 2, (255, 255, 255))

   pygame.display.flip()

pygame.quit()
