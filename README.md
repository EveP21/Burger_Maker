# Burger Maker

Juego en Python con Pygame donde controlas el pan inferior de una hamburguesa y debes atrapar los ingredientes correctos de cada orden.

## Instalar dependencias

```powershell
python -m pip install -r requirements.txt
Ejecutar juego
python main.py
Correr auditoría express
python -m py_compile main.py settings.py assets.py recipe.py audio.pypython tests\smoke_test.py
Controles


Flecha izquierda: mover a la izquierda


Flecha derecha: mover a la derecha


P: pausar


R: reiniciar cuando pierdes


Reglas


Atrapa solo los ingredientes pedidos en la receta.


Si atrapas un ingrediente incorrecto o excluido, pierdes una vida.


Si se te pasa cualquier objeto que cae, pierdes una vida.


Cuando completes la receta, atrapa el pan superior.


Si atrapas el pan superior antes de completar la receta, pierdes una vida.


Si se te pasa el pan superior, pierdes una vida.


Tienes 3 vidas.


Cada nivel aumenta la dificultad.


El juego sube de nivel infinitamente.


Variables principales
score = 0ingredients = 0lives = 3
Assets esperados
Sprites:
assets/imagenes/background.pngassets/imagenes/pan_abajo.pngassets/imagenes/pan_arriba.pngassets/imagenes/carne.pngassets/imagenes/lechuga.pngassets/imagenes/tomate.pngassets/imagenes/queso.pngassets/imagenes/tocino.png
Música:
assets/music/background.mp3
El juego funciona aunque no existan los archivos, usando dibujos simples como respaldo.
