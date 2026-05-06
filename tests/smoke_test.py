import os
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def check_file(path):
    full_path = os.path.join(ROOT, path)
    if not os.path.exists(full_path):
        raise AssertionError(f"Falta archivo: {path}")

def check_import(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        raise AssertionError(f"No se pudo importar: {module_name}")

def main():
    required_files = [
        "main.py",
        "settings.py",
        "assets.py",
        "recipe.py",
        "audio.py",
        "requirements.txt",
    ]

    for file in required_files:
        check_file(file)

    check_import("pygame")
    check_import("settings")
    check_import("assets")
    check_import("recipe")
    check_import("audio")

    import settings
    import recipe

    assert settings.WIDTH == 1280, "WIDTH debe ser 1280"
    assert settings.HEIGHT == 720, "HEIGHT debe ser 720"
    assert settings.START_SCORE == 0, "score debe iniciar en 0"
    assert settings.START_INGREDIENTS == 0, "ingredients debe iniciar en 0"
    assert settings.START_LIVES == 3, "lives debe iniciar en 3"
    assert len(settings.INGREDIENT_DATA) >= 5, "Deben existir al menos 5 ingredientes"

    test_recipe = recipe.generate_recipe(1)

    assert "required" in test_recipe, "La receta debe tener ingredientes requeridos"
    assert "avoid" in test_recipe, "La receta debe tener ingredientes excluidos"
    assert "collected" in test_recipe, "La receta debe llevar control de recolectados"
    assert len(test_recipe["required"]) >= 2, "La receta inicial debe pedir mínimo 2 ingredientes"

    print("SMOKE TEST OK: archivos, imports, settings y recetas funcionan.")

if __name__ == "__main__":
    main()
