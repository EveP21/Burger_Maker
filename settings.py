from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
SPRITE_FOLDER = ASSET_DIR / "sprites"
MUSIC_FILE = ASSET_DIR / "music" / "background.mp3"

WIDTH = 1280
HEIGHT = 720
FPS = 60

GAME_TITLE = "Burger Maker"

START_SCORE = 0
START_INGREDIENTS = 0
START_LIVES = 3
START_LEVEL = 1

ROUND_TIME = 35
BASE_FALL_SPEED = 4
SPEED_PER_LEVEL = 0.45
BASE_SPAWN_DELAY = 55
MIN_SPAWN_DELAY = 18

PADDLE_WIDTH = 220
PADDLE_HEIGHT = 70
PADDLE_SPEED = 11

INGREDIENT_SIZE = (86, 58)
TOP_BUN_SIZE = (110, 62)

BACKGROUND_SPRITE = "background.png"
BOTTOM_BUN_SPRITE = "pan_abajo.png"

INGREDIENT_DATA = {
    "carne": {
        "label": "Carne",
        "points": 15,
        "color": (105, 55, 30),
        "sprite": "carne.png",
    },
    "lechuga": {
        "label": "Lechuga",
        "points": 10,
        "color": (70, 190, 80),
        "sprite": "lechuga.png",
    },
    "tomate": {
        "label": "Tomate",
        "points": 12,
        "color": (220, 45, 45),
        "sprite": "tomate.png",
    },
    "queso": {
        "label": "Queso",
        "points": 14,
        "color": (255, 220, 55),
        "sprite": "queso.png",
    },
    "tocino": {
        "label": "Tocino",
        "points": 18,
        "color": (190, 70, 65),
        "sprite": "tocino.png",
    },
}

TOP_BUN = {
    "label": "Pan superior",
    "points": 40,
    "color": (235, 170, 90),
    "sprite": "pan_arriba.png",
}

BOTTOM_BUN = {
    "label": "Pan inferior",
    "color": (230, 155, 75),
    "sprite": BOTTOM_BUN_SPRITE,
}
