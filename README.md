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
| F11 | Cambiar entre pantalla completa y ventana |

El juego abre en pantalla completa: se dibuja en 1280×720 y se agranda a la pantalla sin deformarse. Para que abra en ventana, poner `PANTALLA_COMPLETA = False` en `config.py`.

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

Cada escena elige cómo se ve con `"diseno"` en su nodo (por defecto `pink_palace`). Hoy existen `pink_palace`, `exploracion`, `exploracion_derecha` (los paneles a la derecha; con `"espejo": true` el fondo se voltea para que la acción quede a la izquierda; así están las escenas del fin del mundo y el estudio del cap. 6, todo el cap. 7, la cocina del cap. 8 y la casa torcida y el mundo gris del cap. 9), `libreta` (hoja de cuaderno, cap01_n03 y cap01_m01) y `puerta` (puerta tallada, cap01_n04 y cap01_n05). Cada diseño es un archivo en `interfaz/disenos/` y se arma con las piezas de `interfaz/piezas.py`: paneles que se ajustan solos al texto, opciones y barra de controles. Para crear uno nuevo, ver las instrucciones en `interfaz/disenos/__init__.py`. Cada diseño tiene un dueño y se edita solo; `piezas.py` es compartido, así que si se cambia hay que avisar.

## Escenas del capítulo 5

Todas usan el diseño `exploracion` y un fondo en pixel art de `interfaz/fondos/`, igual que los capítulos 1 al 4. Reutilizan a Coraline (impermeable y pijama), el gato, las vecinas, la mamá y la otra madre de `personajes.py`, y los cuartos de `cocina_sola`, `regreso_niebla`, `sala_actrices` y `despedida_otros`.

| Nodo | Fondo | Qué se ve |
|---|---|---|
| `cap05_n01` | `cena_sola` | La cocina de noche, Coraline en pijama cenando sola bajo el foco |
| `cap05_r01` | `jardin_noche` | La casona de noche, con viento; solo las ventanas de Coraline prendidas |
| `cap05_n02` | `recortes_vecinas` | Las vecinas con su álbum y recortes de periódico; nadie le hace caso a Coraline |
| `cap05_r02` | `te_actrices` | (reutilizado del cap. 2) El té con las vecinas |
| `cap05_n03`, `cap05_r03`, `cap05_r04` | `espejo_pasillo` | El pasillo de la casa y el gato sentado frente al espejo |
| `cap05_n04` | `espejo_padres` | Los papás pálidos dentro del espejo; el papá escribe AYÚDANOS con el dedo |
| `cap05_n05` | `valentia_gato` | El cuarto de noche, el teléfono, el gato en la cama y el recuerdo de las avispas |
| `cap05_n06`, `cap05_r05` | `bienvenida_otra_madre` | La otra madre con los brazos abiertos; el gato le susurra desde el rincón |

En `personajes.py` se agregó la pose `"brazos_abiertos"` de la otra madre; las poses que ya existían no cambiaron.

## Escenas del capítulo 6

Igual que el capítulo 5: diseño `exploracion` y un fondo en pixel art de `interfaz/fondos/`. Cada rama usa el fondo de su escena canónica.

| Nodo | Fondo | Qué se ve |
|---|---|---|
| `cap06_n01`, `cap06_r01` | `cuarto_manana` | El otro cuarto de mañana: sol por la ventana, cama deshecha y el armario abierto con la ropa nueva; Coraline en pijama |
| `cap06_n02`, `cap06_r02` | `fin_del_mundo` | Detrás de la casa rosa los árboles se vuelven dibujos a medio hacer y todo se borra en blanco; Coraline y el gato |
| `cap06_n03`, `cap06_r03` | `estudio_otro_padre` | El otro padre sentado detrás de un escritorio vacío, susurrando; libros sin título y una ventana que solo muestra blanco |
| `cap06_n04`, `cap06_r04` | `espejo_otra_madre` | Pasillo lila con un espejo de cuerpo entero; la otra madre ofrece juegos (avión, rompecabezas, pelota) en una burbuja |
| `cap06_n05`, `cap06_r05` | `escarabajo_espejo` | El mismo pasillo con luz rojiza: la otra madre se come un escarabajo y el espejo está abierto como puerta a un hueco negro |

En `personajes.py` se agregaron la pose `"escarabajo"` de la otra madre (con `mano_escarabajo`) y la pose `"quieto"` del otro padre; las poses que ya existían no cambiaron.

## Escenas del capítulo 7

Todo pasa en el hueco detrás del espejo. `hueco_espejo.py` tiene las partes que comparten las cinco escenas: el hueco (`dibujar_hueco`) y los tres niños fantasma (`dibujar_fantasma`: `"capa"`, `"cofia"` y `"pequeno"`). Cada rama usa el fondo de su escena canónica.

| Nodo | Fondo | Qué se ve |
|---|---|---|
| `cap07_n01`, `cap07_r01` | `hueco_espejo` | Coraline encerrada en un hueco de tablas con una pared de vidrio; una mano pálida le roza la mano y del otro lado pasa la sombra de la otra madre |
| `cap07_n02`, `cap07_r02` | `ninos_fantasma` | Los tres niños fantasma flotan alrededor de Coraline y su luz llena la oscuridad |
| `cap07_n03`, `cap07_r03` | `almas_perdidas` | El fantasma de capa piensa en sus almas: tres canicas de vidrio en una nube |
| `cap07_n04`, `cap07_r04` | `advertencia_fantasmas` | Los fantasmas se apagan y se prenden; Coraline recuerda a su papá y las avispas (la nube de `valentia_gato`) |
| `cap07_n05`, `cap07_r05` | `beso_fantasma` | Coraline dormida sobre su suéter con la piedra tibia en la mano; el fantasma pequeño le da un beso y le susurra que mire por la piedra |

## Escenas del capítulo 8

Cada rama usa el fondo de su escena canónica. La cocina es la de `otra_cocina` (cap. 3), el cuarto el de `otro_cuarto` (cap. 3) y el teatro el de `teatro_vecinas` (cap. 4).

| Nodo | Fondo | Qué se ve |
|---|---|---|
| `cap08_n01`, `cap08_r01` | `desayuno_otra_madre` | El desayuno increíble (hot cakes, chocolate, jugo); a la otra madre le brillan los botones de emoción |
| `cap08_n02`, `cap08_r02` | `trato_juego` | La otra madre jura con la mano en alto; en una nube, una balanza: los papás y las almas contra dos botones, aguja e hilo |
| `cap08_m01` | `caja_juguetes` | Coraline voltea la caja de juguetes: las canicas salen rodando por el tapete y la piedra se mece colgada de su cordón |
| `cap08_n03`, `cap08_r03` | `vista_piedra` | Desde los ojos de Coraline: el tapete de cerca y la piedra en su mano. Por el agujero todo se ve gris (como es de verdad) menos la canica, que arde como brasa; la piedra recorre el tapete hasta encontrarla |
| `cap08_n04` | `telarana_canica` | De cerca y a oscuras: la mano de Coraline se acerca a la canica de la telaraña, duda y vuelve; detrás se asoma la criatura y su brazo también va por la canica. La telaraña tiembla, las orillas laten como corazón y al final se le abren los ojos a la criatura (ciclo de 10 s) |
| `cap08_r04` | `teatro_abandonado` | El teatro oscuro y con telarañas; la segunda canica pegada en una telaraña enorme y una criatura pálida de dos cuerpos en el escenario |
| `cap08_n05`, `cap08_r05` | `huida_teatro` | Coraline corre con las dos canicas; los perros la miran con ojos rojos y una voz fantasma le grita que huya |

## Escenas del capítulo 9

Cada rama usa el fondo de su escena canónica. `sotano.py` tiene las partes que comparten las escenas del sótano y el minijuego: el cuarto, la escalera (`punto_escalera`) y lo que queda del otro padre (`dibujar_padre_derretido`).

| Nodo | Fondo | Qué se ve |
|---|---|---|
| `cap09_n01`, `cap09_r01` | `casa_torcida` | La casa rosa (la de `exterior_gato`) medio destenida y ondulando; la otra madre con los brazos cruzados ofrece una pista con corazoncitos |
| `cap09_n02`, `cap09_r02` | `pasillo_sotano` | El pasillo lila vacío; Coraline silba (notitas chuecas) y al fondo la puerta del sótano entreabierta |
| `cap09_n03`, `cap09_r03` | `sotano` | Sótano de piedra húmeda con botellas rotas, pan con moho y un foco que se mece; un montón de cortinas que respira y un pie pálido |
| `cap09_n04`, `cap09_r04` | `padre_derretido` | El otro padre hecho una masa blanca; Coraline le acaricia la cabeza y se le cae un botón |
| `cap09_m01` | `sotano_cazando` | La masa de pie, tanteando a ciegas; Coraline quieta a media escalera |
| `cap09_n05`, `cap09_r05` | `mundo_gris` | Afuera todo es gris, con árboles de papel; lo único con color es la lucecita de valor en el pecho de Coraline |

En `personajes.py` se agregó la pose `"brazos_cruzados"` de la otra madre.

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
| Buscar con la piedra (`canicas_piedra`) | Pixel art: el tapete del otro cuarto visto desde arriba, a oscuras. El mouse es la piedra: solo por su agujero hay luz y la canica del alma arde como brasa. Cada canica falsa quita 3 segundos y queda tachada | Cap. 8 |
| Buscar con la piedra (`buscar`) | La pantalla está a oscuras; el mouse es la piedra y solo a través de ella brilla la canica verdadera | Cap. 10 |
| Sube sin que te oiga (`escalera_sotano`) | Pixel art: el sótano. Mantener Espacio o el clic para subir la escalera; cuando el otro padre se detiene a escuchar hay que soltar. Si te oye, se lanza y resbalas (3 vidas) | Cap. 9 |
| Escapar (`esquivar`) | Guiar a Coraline con el mouse esquivando enemigos | Cap. 4 (sombras), cap. 12 (la mano) |
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
