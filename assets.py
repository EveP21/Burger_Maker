import os
import pygame
from settings import (
    WIDTH,
    HEIGHT,
    SPRITE_FOLDER,
    INGREDIENT_DATA,
    INGREDIENT_SIZE,
    TOP_BUN,
    TOP_BUN_SIZE,
    BOTTOM_BUN,
    BOTTOM_BUN_SPRITE,
    BACKGROUND_SPRITE,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
)


def load_image(path, size=None):
    path = os.fspath(path)
    if not os.path.exists(path) or os.path.getsize(path) <= 2:
        return None

    try:
        image = pygame.image.load(path).convert_alpha()
        if size is not None:
            image = pygame.transform.smoothscale(image, size)
        return image
    except pygame.error:
        return None


def _font(size):
    if pygame.font.get_init():
        return pygame.font.SysFont("arial", size, bold=True)
    return None


def _draw_text(surface, text, size, color):
    font = _font(size)
    if font is None:
        return
    label = font.render(text, True, color)
    rect = label.get_rect(center=surface.get_rect().center)
    surface.blit(label, rect)


def make_background():
    surface = pygame.Surface((WIDTH, HEIGHT)).convert()
    surface.fill((28, 29, 34))
    for y in range(0, HEIGHT, 90):
        pygame.draw.rect(surface, (34, 36, 43), (0, y, WIDTH, 45))
    return surface


def make_bun(size, top=False):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    w, h = size
    bun_color = TOP_BUN["color"] if top else BOTTOM_BUN["color"]
    shadow = (120, 75, 35)

    if top:
        pygame.draw.ellipse(surface, shadow, (5, 9, w - 10, h - 9))
        pygame.draw.ellipse(surface, bun_color, (5, 2, w - 10, h - 14))
        for x, y in [(w * 0.30, h * 0.25), (w * 0.50, h * 0.17), (w * 0.68, h * 0.30)]:
            pygame.draw.ellipse(surface, (255, 235, 170), (int(x), int(y), 8, 4))
    else:
        pygame.draw.ellipse(surface, shadow, (4, h * 0.22, w - 8, h * 0.56))
        pygame.draw.ellipse(surface, bun_color, (4, h * 0.10, w - 8, h * 0.56))
        pygame.draw.rect(surface, bun_color, (12, h * 0.37, w - 24, h * 0.32), border_radius=16)

    return surface


def make_ingredient(name, data):
    surface = pygame.Surface(INGREDIENT_SIZE, pygame.SRCALPHA)
    w, h = INGREDIENT_SIZE
    color = data["color"]

    if name == "lechuga":
        points = [(5, h // 2), (18, 14), (32, h // 2), (48, 14), (64, h // 2), (82, 20), (78, 45), (10, 48)]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.lines(surface, (30, 120, 45), False, points, 3)
    elif name == "tomate":
        pygame.draw.circle(surface, color, (w // 2, h // 2), 25)
        pygame.draw.circle(surface, (255, 120, 120), (w // 2 - 8, h // 2 - 7), 7)
        pygame.draw.circle(surface, (255, 120, 120), (w // 2 + 10, h // 2 + 6), 7)
    elif name == "queso":
        points = [(8, 10), (78, 18), (66, 52), (16, 45)]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.circle(surface, (210, 165, 30), (30, 28), 5)
        pygame.draw.circle(surface, (210, 165, 30), (55, 35), 4)
    elif name == "tocino":
        pygame.draw.rect(surface, color, (10, 14, 66, 13), border_radius=7)
        pygame.draw.rect(surface, (245, 150, 120), (10, 31, 66, 13), border_radius=7)
        pygame.draw.line(surface, (120, 35, 35), (16, 21), (72, 21), 3)
        pygame.draw.line(surface, (120, 35, 35), (16, 38), (72, 38), 3)
    else:
        pygame.draw.ellipse(surface, (60, 30, 15), (8, 14, w - 16, h - 22))
        pygame.draw.ellipse(surface, color, (12, 10, w - 24, h - 20))

    return surface


def load_assets():
    assets = {}

    assets["background"] = load_image(SPRITE_FOLDER / BACKGROUND_SPRITE, (WIDTH, HEIGHT)) or make_background()
    assets["bottom_bun"] = load_image(SPRITE_FOLDER / BOTTOM_BUN_SPRITE, (PADDLE_WIDTH, PADDLE_HEIGHT)) or make_bun(
        (PADDLE_WIDTH, PADDLE_HEIGHT), top=False
    )
    assets["top_bun"] = load_image(SPRITE_FOLDER / TOP_BUN["sprite"], TOP_BUN_SIZE) or make_bun(TOP_BUN_SIZE, top=True)

    for name, data in INGREDIENT_DATA.items():
        assets[name] = load_image(SPRITE_FOLDER / data["sprite"], INGREDIENT_SIZE) or make_ingredient(name, data)

    return assets
