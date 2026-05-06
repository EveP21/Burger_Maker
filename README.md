# Burger Maker

Juego en Python con Pygame donde controlas el pan inferior de una hamburguesa y atrapas los ingredientes correctos de cada orden.

## Instalar dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar

```powershell
python main.py
```

## Validar

```powershell
python -m py_compile main.py settings.py assets.py recipe.py audio.py tests\smoke_test.py
python tests\smoke_test.py
```

## Controles

- Flecha izquierda / A: mover a la izquierda
- Flecha derecha / D: mover a la derecha
- P: pausar
- R: reiniciar
- ESC: salir

## Assets

El juego busca sprites en:

```text
assets/sprites/background.png
assets/sprites/pan_abajo.png
assets/sprites/pan_arriba.png
assets/sprites/carne.png
assets/sprites/lechuga.png
assets/sprites/tomate.png
assets/sprites/queso.png
assets/sprites/tocino.png
```

Si faltan sprites o alguno está corrupto, el juego usa dibujos generados como respaldo. Por eso esta versión sí corre aunque todavía falten sprites finales.
