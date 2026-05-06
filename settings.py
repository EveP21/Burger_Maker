WIDTH = 1280
HEIGHT = 720
FPS = 60

GAME_TITLE = "Burger Rush"

START_SCORE = 0
START_INGREDIENTS = 0
START_LIVES = 3

ROUND_TIME = 35
BASE_FALL_SPEED = 4
SPEED_PER_LEVEL = 0.45
BASE_SPAWN_DELAY = 55
MIN_SPAWN_DELAY = 18

PADDLE_WIDTH = 190
PADDLE_HEIGHT = 55
PADDLE_SPEED = 10

SPRITE_FOLDER = "assets/sprites"
MUSIC_FILE = "assets/music/background.mp3"

INGREDIENT_DATA = {
   "carne": {
       "points": 15,
       "color": (105, 55, 30),
       "sprite": "carne.png"
   },
   "lechuga": {
       "points": 10,
       "color": (70, 190, 80),
       "sprite": "lechuga.png"
   },
   "tomate": {
       "points": 12,
       "color": (220, 45, 45),
       "sprite": "tomate.png"
   },
   "queso": {
       "points": 14,
       "color": (255, 220, 55),
       "sprite": "queso.png"
   },
   "tocino": {
       "points": 18,
       "color": (190, 70, 65),
       "sprite": "tocino.png"
   }
}

TOP_BUN = {
   "points": 40,
   "color": (235, 170, 90),
   "sprite": "pan_arriba.png"
}

BOTTOM_BUN_SPRITE = "pan_abajo.png"
BACKGROUND_SPRITE = "background.png"
