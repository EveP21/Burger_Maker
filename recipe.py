import random
from settings import INGREDIENT_DATA

INGREDIENT_TYPES = list(INGREDIENT_DATA.keys())

def generate_recipe(level):
   required_count = min(len(INGREDIENT_TYPES), 2 + level // 2)
   required = random.sample(INGREDIENT_TYPES, required_count)

   avoid_options = [item for item in INGREDIENT_TYPES if item not in required]
   avoid_count = min(len(avoid_options), level // 2)
   avoid = random.sample(avoid_options, avoid_count)

   return {
       "required": required,
       "avoid": avoid,
       "collected": {item: 0 for item in required}
   }

def collect_required(recipe, ingredient):
   if ingredient in recipe["collected"]:
       recipe["collected"][ingredient] = 1

def is_recipe_complete(recipe):
   return all(recipe["collected"][item] >= 1 for item in recipe["required"])
