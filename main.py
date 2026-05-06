import random
import sys
import pygame

from settings import *
from assets import load_assets
from audio import start_music
from recipe import generate_recipe, collect_required, is_recipe_complete


class FallingItem:
    def __init__(self, kind, image, x, y, speed):
        self.kind = kind
        self.image = image
        self.rect = image.get_rect(topleft=(int(x), int(y)))
        self.speed = speed

    def update(self):
        self.rect.y += int(self.speed)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class BurgerMakerGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 42, bold=True)
        self.font = pygame.font.SysFont("arial", 25, bold=True)
        self.font_small = pygame.font.SysFont("arial", 19)
        self.assets = load_assets()
        start_music()
        self.reset()

    def reset(self):
        self.score = START_SCORE
        self.ingredients = START_INGREDIENTS
        self.lives = START_LIVES
        self.level = START_LEVEL
        self.recipe = generate_recipe(self.level)
        self.falling_items = []
        self.spawn_timer = 0
        self.paddle = self.assets["bottom_bun"].get_rect(midbottom=(WIDTH // 2, HEIGHT - 26))
        self.paused = False
        self.game_over = False
        self.message = "Atrapa los ingredientes de la receta."
        self.message_timer = 180

    def set_message(self, text, frames=150):
        self.message = text
        self.message_timer = frames

    def lose_life(self, reason):
        if self.game_over:
            return
        self.lives -= 1
        self.set_message(reason, 170)
        if self.lives <= 0:
            self.game_over = True
            self.set_message("Juego terminado. Presiona R para reiniciar.", 999999)

    def next_level(self):
        self.score += self.level * 10
        self.level += 1
        self.recipe = generate_recipe(self.level)
        self.falling_items.clear()
        self.spawn_timer = 25
        self.set_message(f"Nivel {self.level}. Nueva orden.", 180)

    def spawn_delay(self):
        return max(MIN_SPAWN_DELAY, BASE_SPAWN_DELAY - self.level * 3)

    def spawn_item(self):
        recipe_complete = is_recipe_complete(self.recipe)

        if recipe_complete and random.random() < 0.45:
            kind = "__top_bun__"
            image = self.assets["top_bun"]
        else:
            kind = random.choice(list(INGREDIENT_DATA.keys()))
            image = self.assets[kind]

        margin = max(24, image.get_width() // 2)
        x = random.randint(margin, WIDTH - margin - image.get_width())
        y = -image.get_height() - 8
        speed = BASE_FALL_SPEED + (self.level - 1) * SPEED_PER_LEVEL + random.uniform(0, 1.25)
        self.falling_items.append(FallingItem(kind, image, x, y, speed))

    def handle_catch(self, item):
        if item.kind == "__top_bun__":
            if is_recipe_complete(self.recipe):
                self.score += TOP_BUN["points"]
                self.next_level()
            else:
                self.lose_life("Todavia no completes la receta. No atrapes el pan superior.")
            return

        if item.kind in self.recipe["required"]:
            already_collected = self.recipe["collected"].get(item.kind, 0) >= 1
            collect_required(self.recipe, item.kind)
            self.score += INGREDIENT_DATA[item.kind]["points"]
            if not already_collected:
                self.ingredients += 1
            label = INGREDIENT_DATA[item.kind]["label"]
            if is_recipe_complete(self.recipe):
                self.set_message("Receta completa. Ahora atrapa el pan superior.", 180)
            else:
                self.set_message(f"Correcto: {label}", 90)
        else:
            label = INGREDIENT_DATA[item.kind]["label"]
            self.lose_life(f"Ingrediente incorrecto: {label}")

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused
                if event.key == pygame.K_r:
                    self.reset()

    def update(self):
        if self.game_over or self.paused:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.x += PADDLE_SPEED
        self.paddle.clamp_ip(self.screen.get_rect())

        if self.spawn_timer <= 0:
            self.spawn_item()
            self.spawn_timer = self.spawn_delay()
        else:
            self.spawn_timer -= 1

        for item in self.falling_items[:]:
            item.update()

            if item.rect.colliderect(self.paddle):
                self.falling_items.remove(item)
                self.handle_catch(item)
                continue

            if item.rect.top > HEIGHT:
                self.falling_items.remove(item)
                if item.kind == "__top_bun__":
                    self.lose_life("Se te paso el pan superior.")
                else:
                    self.lose_life("Se te paso un ingrediente.")

        if self.message_timer > 0:
            self.message_timer -= 1

    def draw_text(self, text, font, color, pos, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = pos
        else:
            rect.topleft = pos
        self.screen.blit(surface, rect)

    def draw_hud(self):
        panel = pygame.Rect(24, 22, 420, 210)
        pygame.draw.rect(self.screen, (18, 19, 24), panel, border_radius=18)
        pygame.draw.rect(self.screen, (75, 80, 95), panel, 2, border_radius=18)

        self.draw_text(f"Score: {self.score}", self.font, (245, 245, 245), (44, 38))
        self.draw_text(f"Vidas: {self.lives}", self.font, (245, 245, 245), (225, 38))
        self.draw_text(f"Nivel: {self.level}", self.font, (245, 245, 245), (44, 74))
        self.draw_text(f"Ingredientes: {self.ingredients}", self.font, (245, 245, 245), (225, 74))

        self.draw_text("Orden:", self.font, (255, 220, 120), (44, 116))
        y = 148
        for ingredient in self.recipe["required"]:
            checked = self.recipe["collected"].get(ingredient, 0) >= 1
            symbol = "OK" if checked else "--"
            label = INGREDIENT_DATA[ingredient]["label"]
            color = (120, 240, 150) if checked else (235, 235, 235)
            self.draw_text(f"{symbol} {label}", self.font_small, color, (58, y))
            y += 25

        if self.recipe["avoid"]:
            avoid_labels = ", ".join(INGREDIENT_DATA[item]["label"] for item in self.recipe["avoid"])
            self.draw_text(f"Evita: {avoid_labels}", self.font_small, (255, 145, 145), (230, 116))

        if self.message_timer > 0 and self.message:
            self.draw_text(self.message, self.font, (255, 255, 255), (WIDTH // 2, 35), center=True)

        if is_recipe_complete(self.recipe) and not self.game_over:
            self.draw_text("RECETA COMPLETA: ATRAPA EL PAN SUPERIOR", self.font, (255, 230, 110), (WIDTH // 2, 74), center=True)

        self.draw_text("←/A y →/D mover | P pausa | R reiniciar | ESC salir", self.font_small, (220, 220, 220), (WIDTH - 500, HEIGHT - 34))

    def draw_overlay(self, title, subtitle):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        self.draw_text(title, self.font_big, (255, 255, 255), (WIDTH // 2, HEIGHT // 2 - 45), center=True)
        self.draw_text(subtitle, self.font, (235, 235, 235), (WIDTH // 2, HEIGHT // 2 + 10), center=True)

    def draw(self):
        self.screen.blit(self.assets["background"], (0, 0))

        for item in self.falling_items:
            item.draw(self.screen)

        self.screen.blit(self.assets["bottom_bun"], self.paddle)
        self.draw_hud()

        if self.paused:
            self.draw_overlay("PAUSA", "Presiona P para continuar")
        if self.game_over:
            self.draw_overlay("GAME OVER", "Presiona R para reiniciar")

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.process_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    BurgerMakerGame().run()
