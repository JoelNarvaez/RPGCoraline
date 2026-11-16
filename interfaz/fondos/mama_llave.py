"""FONDO DIBUJADO CON CODIGO: LA MAMA DE CORALINE CON LA LLAVE (CUERPO COMPLETO).

La mama acaba de abrir la puerta pequena: detras solo hay ladrillos. Ella
aparece grande junto al hueco, ensenando la llave negra, y Coraline esta al
frente, cortada por la orilla de abajo (es la imagen del menu,
coraline_menu.jpg, sin su fondo oscuro). La mama es el sprite de
personajes.py agrandado 2 veces, para que se vea del tamano de esa imagen.
Se usa en cap01_n05.

La mama queda a la derecha porque a la izquierda va el panel de texto.
"""

import os

import pygame

import config

from interfaz.fondos.pintura import ANCHO, ALTO
from interfaz.fondos.pintura import mezclar, degradado, brillo, orillas_oscuras, mostrar
from interfaz.fondos import personajes

Y_PISO = 330

# HUECO DE LA PUERTA CON LADRILLOS, DETRAS DE LA MAMA
HUECO = pygame.Rect(424, 150, 120, Y_PISO - 150)

# LA MAMA: CENTRO DE SUS PIES, MIRANDO A CORALINE (A LA IZQUIERDA), AGRANDADA x2
X_MAMA = 568
TAMANO_MAMA = 2

# CORALINE: IMAGEN DEL MENU, AL FRENTE Y A LA IZQUIERDA DE SU MAMA
IMAGEN_CORALINE = "coraline_menu.jpg"
RECORTE_CORALINE = pygame.Rect(492, 52, 418, 716)    # DONDE ESTA ELLA DENTRO DE LA IMAGEN
ALTO_CORALINE = 200                                  # ALTO EN EL LIENZO
X_CORALINE = 380                                     # ORILLA IZQUIERDA EN EL LIENZO
COLOR_FONDO_IMAGEN = (12, 21, 37)

COLOR_PARED = (52, 112, 116)
COLOR_LLAVE = (16, 14, 18)

CAPAS = {}


# --------------------------------------------------
# PARTE FIJA: FONDO
# --------------------------------------------------

def dibujar_fondo(lienzo: pygame.Surface) -> None:

    """PARED VERDE AZULADA, PISO OSCURO, EL HUECO CON LADRILLOS Y LA HOJA ABIERTA."""

    degradado(lienzo, pygame.Rect(0, 0, ANCHO, Y_PISO), (18, 40, 44), COLOR_PARED, 28)
    degradado(lienzo, pygame.Rect(0, Y_PISO, ANCHO, ALTO - Y_PISO), (30, 58, 64), (12, 24, 30), 4)

    pygame.draw.rect(lienzo, (34, 78, 82), (0, Y_PISO - 6, ANCHO, 6))
    pygame.draw.line(lienzo, (70, 128, 130), (0, Y_PISO - 7), (ANCHO, Y_PISO - 7))

    # MARCO Y LADRILLOS
    pygame.draw.rect(lienzo, (16, 34, 38), HUECO.inflate(12, 6).move(0, -3))
    pygame.draw.rect(lienzo, (52, 44, 44), HUECO)

    tonos = [(140, 56, 46), (124, 48, 40), (154, 66, 52), (116, 44, 40)]

    fila = 0

    for y in range(HUECO.y, HUECO.bottom, 10):

        desfase = 0 if fila % 2 == 0 else -12

        columna = 0

        for x in range(HUECO.x + desfase, HUECO.right, 24):

            ladrillo = pygame.Rect(x + 1, y + 1, 22, 8).clip(HUECO)

            if ladrillo.width > 0:
                pygame.draw.rect(lienzo, tonos[(fila * 3 + columna) % 4], ladrillo)

            columna = columna + 1

        fila = fila + 1

    # VELO OSCURO SOBRE LOS LADRILLOS Y SOMBRA ARRIBA: QUEDAN ATRAS Y LA MAMA RESALTA
    velo = pygame.Surface(HUECO.size, pygame.SRCALPHA)
    velo.fill((10, 24, 28, 70))
    lienzo.blit(velo, HUECO.topleft)

    sombra = pygame.Surface((HUECO.width, 16), pygame.SRCALPHA)

    for i in range(16):
        pygame.draw.line(sombra, (0, 0, 0, 130 - i * 8), (0, i), (HUECO.width, i))

    lienzo.blit(sombra, HUECO.topleft)

    # HOJA DE LA PUERTA ABIERTA HACIA EL FRENTE (BISAGRA A LA DERECHA)
    x = HUECO.right + 6
    hoja = [(x, HUECO.y - 3), (x + 34, HUECO.y + 10), (x + 34, Y_PISO + 12), (x, Y_PISO)]
    pygame.draw.polygon(lienzo, (86, 76, 74), hoja)
    pygame.draw.polygon(lienzo, (50, 44, 44), hoja, 1)
    pygame.draw.line(lienzo, (112, 100, 96), (x + 34, HUECO.y + 10), (x + 34, Y_PISO + 12), 2)


def es_fondo_imagen(color: pygame.Color) -> bool:

    """TRUE SI EL COLOR SE PARECE AL AZUL CASI NEGRO DEL FONDO DE LA IMAGEN."""

    diferencia = (
        abs(color.r - COLOR_FONDO_IMAGEN[0])
        + abs(color.g - COLOR_FONDO_IMAGEN[1])
        + abs(color.b - COLOR_FONDO_IMAGEN[2])
    )

    return diferencia < 24


def cargar_coraline() -> pygame.Surface:

    """RECORTA A CORALINE DE LA IMAGEN, LA ACHICA Y LE QUITA EL FONDO OSCURO.

    El fondo se borra pintando desde las orillas de arriba, izquierda y derecha
    hacia adentro (como la cubeta de pintura), asi los oscuros de adentro
    (contorno, guantes) no se borran.
    """

    imagen = pygame.image.load(os.path.join(config.RUTA_IMAGENES, IMAGEN_CORALINE))
    imagen = imagen.subsurface(RECORTE_CORALINE)

    ancho = int(RECORTE_CORALINE.width * ALTO_CORALINE / RECORTE_CORALINE.height)

    # scale (Y NO smoothscale) PARA QUE LOS PIXELES QUEDEN NITIDOS
    sprite = pygame.transform.scale(imagen, (ancho, ALTO_CORALINE)).convert_alpha()

    pendientes = []

    for x in range(ancho):
        pendientes.append((x, 0))

    for y in range(ALTO_CORALINE):
        pendientes.append((0, y))
        pendientes.append((ancho - 1, y))

    while len(pendientes) > 0:

        x, y = pendientes.pop()

        if x < 0 or y < 0 or x >= ancho or y >= ALTO_CORALINE:
            continue

        color = sprite.get_at((x, y))

        if color.a == 0 or not es_fondo_imagen(color):
            continue

        sprite.set_at((x, y), (0, 0, 0, 0))

        pendientes.append((x + 1, y))
        pendientes.append((x - 1, y))
        pendientes.append((x, y + 1))
        pendientes.append((x, y - 1))

    return sprite


def dibujar_coraline(lienzo: pygame.Surface) -> None:

    """CORALINE AL FRENTE: SUS MANOS QUEDAN EN LA ORILLA DE ABAJO DE LA PANTALLA."""

    lienzo.blit(cargar_coraline(), (X_CORALINE, ALTO - ALTO_CORALINE))


def llave_aro() -> tuple:

    """EL ARO DE LA LLAVE QUEDA EN LA MANO DE LA MAMA."""

    return personajes.manos_mama(X_MAMA, Y_PISO, False, TAMANO_MAMA)


def dibujar_llave(lienzo: pygame.Surface, color: tuple, x: int, y: int, grueso: int) -> None:

    """LA FORMA DE LA LLAVE: ARO EN LA MANO, VARILLA Y DIENTES APUNTANDO A CORALINE.
    grueso 0 ES LA LLAVE; grueso 1 ES LA ORILLA CLARA QUE VA DETRAS PARA QUE RESALTE."""

    pygame.draw.circle(lienzo, color, (x, y), 9 + grueso)
    pygame.draw.rect(lienzo, color, (x - 50 - grueso, y - 3 - grueso, 50 + grueso * 2, 6 + grueso * 2))
    pygame.draw.rect(lienzo, color, (x - 50 - grueso, y + 2 - grueso, 6 + grueso * 2, 11 + grueso * 2))
    pygame.draw.rect(lienzo, color, (x - 40 - grueso, y + 2 - grueso, 5 + grueso * 2, 8 + grueso * 2))


def dibujar_mama(lienzo: pygame.Surface) -> None:

    """LA MAMA Y, ENCIMA DE SU MANO, LA LLAVE NEGRA CON UNA ORILLA CLARA."""

    personajes.dibujar_mama(lienzo, X_MAMA, Y_PISO, False, TAMANO_MAMA)

    x, y = llave_aro()

    dibujar_llave(lienzo, (176, 168, 196), x, y, 1)
    dibujar_llave(lienzo, COLOR_LLAVE, x, y, 0)
    pygame.draw.circle(lienzo, (226, 196, 170), (x, y), 4)                      # hueco del aro (se ve el sueter)
    pygame.draw.line(lienzo, (80, 76, 92), (x - 46, y - 2), (x - 10, y - 2))      # brillito


def dibujar_luces(lienzo: pygame.Surface) -> None:

    """LUZ FRIA DESDE LA IZQUIERDA, LUZ CALIDA DE LA COCINA DESDE LA DERECHA."""

    brillo(lienzo, (430, 150), 140, (120, 210, 220), 45)
    brillo(lienzo, (640, 200), 150, (255, 196, 120), 70)

    orillas_oscuras(lienzo)


def crear_fijo() -> pygame.Surface:

    lienzo = pygame.Surface((ANCHO, ALTO))

    dibujar_fondo(lienzo)
    dibujar_mama(lienzo)
    dibujar_coraline(lienzo)
    dibujar_luces(lienzo)

    return lienzo


# --------------------------------------------------
# LO QUE SE MUEVE
# --------------------------------------------------

def dibujar_destello_llave(lienzo: pygame.Surface, tiempo: float) -> None:

    """UN BRILLO QUE RECORRE LA LLAVE CADA 3 SEGUNDOS."""

    fase = tiempo % 3

    if fase < 0.4:

        aro = llave_aro()
        x = aro[0] - 10 - int(fase * 90)
        y = aro[1] - 4

        pygame.draw.line(lienzo, (255, 250, 220), (x - 3, y), (x + 3, y))
        pygame.draw.line(lienzo, (255, 250, 220), (x, y - 3), (x, y + 3))


def dibujar(ventana: pygame.Surface) -> None:

    """DIBUJA LA ESCENA COMPLETA EN LA VENTANA DEL JUEGO."""

    if "fijo" not in CAPAS:
        CAPAS["fijo"] = crear_fijo()

    tiempo = pygame.time.get_ticks() / 1000

    lienzo = CAPAS["fijo"].copy()

    dibujar_destello_llave(lienzo, tiempo)

    mostrar(ventana, lienzo)
