# coraline-rpg

RPG de texto en Python con **pygame** basado en *Coraline* de Neil Gaiman: 300 decisiones, una ruta canónica de 70, bifurcaciones que regresan a la historia principal, inventario, estadísticas, varios finales, guardado de partida y animaciones (texto que se escribe solo, fundidos entre escenas).

Proyecto escolar con fines académicos. *Coraline* es obra de Neil Gaiman. Este proyecto no es oficial.

## Requisitos

- Python 3.10 o superior
- pygame-ce (se instala con `requirements.txt`)

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## Cómo jugar

```bash
python main.py
```

| Tecla | Acción |
|---|---|
| Clic o 1-4 | Elegir opción |
| Clic o Espacio | Mostrar el texto completo |
| G | Guardar partida |
| I | Inventario y estadísticas |
| Esc | Volver al menú |
| Mouse / Espacio | Jugar los minijuegos |

## Cómo verificar la historia

```bash
python -m herramientas.verificador
```

También revisa que el texto de cada escena quepa en su diseño.

## Cómo probar una escena sin jugar desde el inicio

```bash
python -m herramientas.vista_previa cap08_n03             # abre el juego en esa escena
python -m herramientas.vista_previa cap08_n03 --captura   # guarda capturas/cap08_n03.png
```

## Diseños de escena

Cada escena elige cómo se ve con `"diseno"` en su nodo (por defecto `pink_palace`). Hoy existen `pink_palace`, `exploracion`, `libreta` (hoja de cuaderno, cap01_n03 y cap01_m01) y `puerta` (puerta tallada, cap01_n04 y cap01_n05). Cada diseño es un archivo en `interfaz/disenos/` y se arma con las piezas de `interfaz/piezas.py`: paneles que se ajustan solos al texto, opciones y barra de controles. Para crear uno nuevo, ver las instrucciones en `interfaz/disenos/__init__.py`. Cada diseño tiene un dueño y se edita solo; `piezas.py` es compartido, así que si se cambia hay que avisar.

## Estructura

```
main.py                 Ventana y ciclo principal de pygame            (Persona A)
config.py               Tamaño de ventana, colores, rutas, límites     (compartido)
juego/                  Lógica, sin pygame
  motor.py              Carga la historia y avanza entre nodos         (Persona A)
  partida.py            Estado de la partida, guardar y cargar         (Persona A)
  inventario.py         Objetos de Coraline                            (Persona B)
  estadisticas.py       Valentía, cordura, confianza del gato          (Persona B)
interfaz/               Todo lo que usa pygame
  dibujo.py             Texto en renglones, botones, imágenes          (Persona B)
  animaciones.py        Máquina de escribir y fundido                  (Persona A)
  pantalla_menu.py      Menú principal                                 (Persona B)
  pantalla_juego.py     Flujo de la escena: clics, teclas, elegir      (Persona A)
  piezas.py             Paneles, texto, opciones y controles           (compartido)
  disenos/              Un archivo por diseño de escena                (cada uno su dueño)
  fondos/               Fondos en pixel art dibujados con código       (cada uno su dueño)
  pantalla_inventario.py  Panel de objetos y estadísticas              (Persona B)
  pantalla_final.py     Pantalla de final                              (Persona B)
  pantalla_minijuego.py Instrucciones, minijuego y resultado           (Persona A)
  figuras.py            Llave, gato, mano... dibujados con código      (Persona B)
  minijuegos/           clic, arrastrar, buscar, esquivar, presionar   (Persona B)
historia/
  cap01.json - cap06.json                                              (Persona A)
  cap07.json - cap13.json                                              (Persona B)
  finales.json                                                         (Persona B)
recursos/               Imágenes, fuentes y sonidos (con licencia libre)
herramientas/
  verificador.py        Cuenta decisiones y busca nodos rotos          (Persona B)
  vista_previa.py       Abre el juego directo en una escena            (compartido)
partidas/               Partidas guardadas (no se suben al repo)
docs/
  formato_nodo.md       Cómo se escribe un nodo de la historia
```

## Minijuegos

En momentos clave de la historia, en lugar de opciones aparece un reto. Ganar o perder cambia lo que pasa después.

| Tipo | Cómo se juega | Dónde |
|---|---|---|
| Recorrer la casa (`recorrido`) | Pixel art: cuarto por cuarto, tocar todas las puertas y ventanas; Coraline camina hacia lo que tocas. Termina en la puerta tallada del salón | Cap. 1 (contar puertas) |
| Abrir la puerta (`llave_puerta`) | Pixel art: la puerta pequeña de cerca; arrastrar la llave helada hasta la cerradura. Pesa (va lenta y se cuelga) y tiembla de frío cerca de la puerta; si se suelta lejos, se cae | Cap. 3 (la llave) |
| Leer las hojas (`taza_te`) | Pixel art: la taza vista desde arriba con el té dando vueltas; encontrar los 9 grumos de hojas entre las motitas. Al final forman una mano | Cap. 2 (hojas de té) |
| Explorar (`clic`) | Encontrar y hacer clic en todas las figuras antes de que se acabe el tiempo | Sin usar por ahora |
| Arrastrar (`arrastrar`) | Llevar un objeto con el mouse hasta su lugar | Cap. 11 (gato), cap. 13 (mantel) |
| Buscar con la piedra (`buscar`) | La pantalla está a oscuras; el mouse es la piedra y solo a través de ella brilla la canica verdadera | Cap. 8, cap. 10 |
| Escapar (`esquivar`) | Guiar a Coraline con el mouse esquivando enemigos | Cap. 4 (sombras), cap. 9 (otro padre), cap. 12 (la mano) |
| Rápido (`presionar`) | Presionar Espacio muy rápido para cerrar la puerta | Cap. 11 |

## Créditos de recursos

Toda imagen, fuente o sonido en `recursos/` debe ser propio o de licencia libre, y se anota aquí con su autor y licencia. No se usan imágenes de la película. Las imágenes vienen de Wikimedia Commons; se recortaron a 16:9 y se les aplicó un filtro oscuro con tono morado para que combinen. Las figuras de los minijuegos (llave, gato, mano, etc.) están dibujadas con código en `interfaz/figuras.py`.

| Archivo | Original | Autor | Licencia |
|---|---|---|---|
| `casa.jpg` | [File:Pałac Schoena Muzeum w Sosnowcu Środuli.jpg](https://commons.wikimedia.org/wiki/File:Pa%C5%82ac_Schoena_Muzeum_w_Sosnowcu_%C5%9Aroduli.jpg) | Krzysztof Popławski | CC BY 3.0 |
| `jardin.jpg` | [File:Castle Gerden (Celina Castle) K 08.jpg](https://commons.wikimedia.org/wiki/File:Castle_Gerden_(Celina_Castle)_K_08.jpg) | Mojmir Churavy | CC0 |
| `pozo.jpg` | [File:Old disused well near Myrstigen trail.jpg](https://commons.wikimedia.org/wiki/File:Old_disused_well_near_Myrstigen_trail.jpg) | W.carter | CC BY 4.0 |
| `salon.jpg` | [File:Living room and fireplace LCCN2014712833.jpg](https://commons.wikimedia.org/wiki/File:Living_room_and_fireplace_LCCN2014712833.jpg) | Bain News Service, publisher | Public domain |
| `pasillo.jpg` | [File:Window at the of the dark hallway at the old abandoned building.jpg](https://commons.wikimedia.org/wiki/File:Window_at_the_of_the_dark_hallway_at_the_old_abandoned_building.jpg) | Shixart1985 | CC BY 2.0 |
| `cocina.jpg` | [File:Colonial kitchen inside settler's cottage.jpg](https://commons.wikimedia.org/wiki/File:Colonial_kitchen_inside_settler%27s_cottage.jpg) | Pseudopanax at English Wikipedia | Public domain |
| `cuarto.jpg` | [File:Antique German farm toys (26585407360).jpg](https://commons.wikimedia.org/wiki/File:Antique_German_farm_toys_(26585407360).jpg) | Thomas Quine | CC BY 2.0 |
| `teatro.jpg` | [File:Monte Carlo Casino theatre interior 1878-79 - Leniaud 2003 p78.jpg](https://commons.wikimedia.org/wiki/File:Monte_Carlo_Casino_theatre_interior_1878-79_-_Leniaud_2003_p78.jpg) | Jean Gilletta / Charles Garnier | Public domain |
| `niebla.jpg` | [File:Solitary tree in dense fog.jpg](https://commons.wikimedia.org/wiki/File:Solitary_tree_in_dense_fog.jpg) | Mar Mkrtchyan | CC0 |
| `espejo.jpg` | [File:Salvage One Antique Store (4363928867).jpg](https://commons.wikimedia.org/wiki/File:Salvage_One_Antique_Store_(4363928867).jpg) | David Hilowitz from San Antonio, USA | CC BY 2.0 |
| `sotano.jpg` | [File:Dickensian interior of the wine vault (27496046772).jpg](https://commons.wikimedia.org/wiki/File:Dickensian_interior_of_the_wine_vault_(27496046772).jpg) | shankar s. from Dubai, united arab emirates | CC BY 2.0 |
| `atico.jpg` | [File:Flickr - Infrogmation - AtticRoofBackVent.jpg](https://commons.wikimedia.org/wiki/File:Flickr_-_Infrogmation_-_AtticRoofBackVent.jpg) | Infrogmation of New Orleans from New Orleans | CC BY 2.0 |
| `prado.jpg` | [File:August, 2008. Flower meadow (lousewort, paintbrush, lupine, arnica, etc) (49449297baa2456391697715183f59d1).JPG](https://commons.wikimedia.org/wiki/File:August,_2008._Flower_meadow_(lousewort,_paintbrush,_lupine,_arnica,_etc)_(49449297baa2456391697715183f59d1).JPG) | Steve Redman (MORA) | Public domain |
| `noche.jpg` | [File:Romantic Morning Athmosphere (153899393).jpeg](https://commons.wikimedia.org/wiki/File:Romantic_Morning_Athmosphere_(153899393).jpeg) | Florian S | CC BY 3.0 |
